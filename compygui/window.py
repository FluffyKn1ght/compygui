"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from sdl2 import SDL_WINDOW_RESIZABLE, SDL_CreateWindow, SDL_HideWindow, SDL_WindowFlags
from sdl2.video import (
    SDL_WINDOW_HIDDEN,
    SDL_WINDOW_SHOWN,
    SDL_WINDOWPOS_CENTERED,
    SDL_WINDOWPOS_UNDEFINED,
    SDL_DestroyWindow,
    SDL_ShowWindow,
    SDL_Window,
)
from compygui.basecomponent import BaseComponent
from compygui.datatypes import Vector2
from compygui.errors import SDLErrorDetector


class WindowPositionFlags:
    def __init__(self, x: SDL_WindowFlags, y: SDL_WindowFlags) -> None:
        self.x: int = x & (SDL_WINDOWPOS_CENTERED | SDL_WINDOWPOS_UNDEFINED)
        self.y: int = y & (SDL_WINDOWPOS_CENTERED | SDL_WINDOWPOS_UNDEFINED)

    @staticmethod
    def centered() -> WindowPositionFlags:
        return WindowPositionFlags(SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED)

    @staticmethod
    def undefined() -> WindowPositionFlags:
        return WindowPositionFlags(SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED)


class Window(BaseComponent):
    def __init__(
        self,
        *args,
        title="Window",
        position: Vector2 | WindowPositionFlags,
        size: Vector2,
        flags: int = SDL_WINDOW_RESIZABLE
    ) -> None:
        super().__init__()

        self._window: SDL_Window | None = None
        self.shown: bool = False

        with SDLErrorDetector(error_info="Failed to create window"):
            self._window = SDL_CreateWindow(
                title.encode("utf-8"),
                position.x,
                position.y,
                size.x,
                size.y,
                flags | SDL_WINDOW_HIDDEN,
            )

    def reparent(self, to: BaseComponent | None) -> None:
        raise NotImplementedError("Cannot reparent Window()")

    def show(self) -> None:
        SDL_ShowWindow(self._window)

    def hide(self) -> None:
        SDL_HideWindow(self._window)

    def destroy(self) -> None:
        SDL_DestroyWindow(self._window)
