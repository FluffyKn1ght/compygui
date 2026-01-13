"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from sdl2 import (
    SDL_RENDERER_PRESENTVSYNC,
    SDL_WINDOW_RESIZABLE,
    SDL_CreateWindow,
    SDL_HideWindow,
    SDL_WindowFlags,
)
from sdl2.render import SDL_RENDERER_ACCELERATED, SDL_CreateRenderer, SDL_Renderer
from sdl2.video import (
    SDL_WINDOW_HIDDEN,
    SDL_WINDOW_SHOWN,
    SDL_WINDOWPOS_CENTERED,
    SDL_WINDOWPOS_UNDEFINED,
    SDL_DestroyWindow,
    SDL_ShowWindow,
    SDL_Window,
)
from compygui.component import Component
from compygui.datatypes import Vector2
from compygui.errors import SDLErrorDetector
from compygui.viewport import Viewport


class WindowPositionFlags:
    """A class that holds two sets of SDL window flags for
    the two different axis.

    x: The X axis.
    y: The Y axis.
    """

    def __init__(self, x: SDL_WindowFlags, y: SDL_WindowFlags) -> None:
        self.x: int = x & (SDL_WINDOWPOS_CENTERED | SDL_WINDOWPOS_UNDEFINED)
        self.y: int = y & (SDL_WINDOWPOS_CENTERED | SDL_WINDOWPOS_UNDEFINED)

    @staticmethod
    def centered() -> WindowPositionFlags:
        """Equivalent to WindowPositionFlags(SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED)"""
        return WindowPositionFlags(SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED)

    @staticmethod
    def undefined() -> WindowPositionFlags:
        """Equivalent to WindowPositionFlags(SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED)"""
        return WindowPositionFlags(SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED)


class Window:
    """An application window.

    The Window() is the second-from-the-top-level object, which means that it has
    to be registered to an ComPyGUIApp() via ComPyGUIApp().register_window()
    to properly render and recieve events. Creating a Window() will automatically
    create an SDL renderer, as well as a Viewport(). Any and all GUIComponents must be
    parented to that viewport to be properly rendered.
    """

    def __init__(
        self,
        *args,
        title="Window",
        position: Vector2 | WindowPositionFlags,
        size: Vector2,
        window_flags: int = SDL_WINDOW_RESIZABLE,
        renderer_flags: int = SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC,
    ) -> None:
        self.destroyed: bool = False

        self._window: SDL_Window | None = None
        self._renderer: SDL_Renderer | None = None

        self.viewport: Viewport = Viewport(window=self)

        self.shown: bool = False

        with SDLErrorDetector(error_info="Failed to create window"):
            self._window = SDL_CreateWindow(
                title.encode("utf-8"),
                position.x,
                position.y,
                size.x,
                size.y,
                window_flags | SDL_WINDOW_HIDDEN,
            )

        with SDLErrorDetector(error_info="Failed to create renderer"):
            self._renderer = SDL_CreateRenderer(self._window, -1, renderer_flags)

    def __del__(self) -> None:
        self.destroy()

    def show(self) -> None:
        SDL_ShowWindow(self._window)

    def hide(self) -> None:
        SDL_HideWindow(self._window)

    def destroy(self) -> None:
        if self.destroyed:
            return

        SDL_DestroyWindow(self._window)
