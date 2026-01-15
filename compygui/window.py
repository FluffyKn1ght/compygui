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
    error,
)
from sdl2.render import (
    SDL_RENDERER_ACCELERATED,
    SDL_CreateRenderer,
    SDL_CreateTextureFromSurface,
    SDL_DestroyRenderer,
    SDL_RenderClear,
    SDL_RenderCopy,
    SDL_RenderPresent,
    SDL_Renderer,
    SDL_Texture,
)
from sdl2.surface import SDL_Surface
from sdl2.video import (
    SDL_WINDOW_HIDDEN,
    SDL_WINDOWPOS_CENTERED,
    SDL_WINDOWPOS_UNDEFINED,
    SDL_DestroyWindow,
    SDL_GetWindowID,
    SDL_GetWindowSurface,
    SDL_ShowWindow,
    SDL_Window,
)
from compygui.component import Component
from compygui.datatypes.vector2 import IVector2
from compygui.datatypes.rgba import RGBAMask
from compygui.errors import SDLError, SDLErrorDetector
from compygui.events import Event, EventOrigin, EventQueue, EventType
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
    create an SDL renderer, as well as a Viewport() to serve as a VCT root.
    Any and all GUIComponents must be parented to that viewport
    to be properly rendered inside the window.

    title: The title of the window
    position: The position of the window on the screen
    size: The size of the window
    window_flags: Flags to be passed to SDL_CreateWindow
    renderer_flags: Flags to be passed to SDL_CreateRenderer
    vp_bit_depth: Viewport surface bit depth
    vp_mask: Viewport RGBA mask/format
    """

    def __init__(
        self,
        *args,
        title="Window",
        position: IVector2 | WindowPositionFlags,
        size: IVector2,
        window_flags: int = SDL_WINDOW_RESIZABLE,
        renderer_flags: int = SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC,
        vp_bit_depth: int = 8,
        vp_mask: RGBAMask = RGBAMask.RGBA(),
        app_event_queue: EventQueue,
    ) -> None:
        self.destroyed: bool = False

        self.size: IVector2 = size

        self._window: SDL_Window
        self._renderer: SDL_Renderer
        self.viewport: Viewport

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

        with SDLErrorDetector(error_info="Failed to create renderer for window"):
            self._renderer = SDL_CreateRenderer(self._window, -1, renderer_flags)

        self.event_queue: EventQueue = EventQueue()
        self.app_events: EventQueue = app_event_queue

        try:
            self.viewport = Viewport(
                size=size,
                mask=vp_mask,
                bit_depth=vp_bit_depth,
                window_events=self.event_queue,
            )
        except SDLError as e:
            raise SDLError(f"Failed to create viewport for window: {e.msg}")

        self.app_events.listen(
            self.on_window_close, EventType.APP_WINDOW_CLOSE, oneshot=True
        )
        self.app_events.listen(self.on_render, EventType.APP_RENDER)

    def __del__(self) -> None:
        self.destroy()

    def _render(self) -> None:
        with SDLErrorDetector(error_info="Error during window re-render"):
            surface: SDL_Surface = SDL_GetWindowSurface(self._window)
            tex: SDL_Texture = SDL_CreateTextureFromSurface(self._renderer, surface)
            SDL_RenderClear(self._renderer)
            SDL_RenderCopy(self._renderer, tex, None, None)
            SDL_RenderPresent(self._renderer)

    def on_window_close(self, event: Event) -> None:
        """Event handler for "window.window_closed" (EventType.WINDOW_WINDOW_CLOSED)"""
        if event.data["window_id"] == SDL_GetWindowID(self._window):
            self.hide()

            self.app_events.fire(
                EventType.WINDOW_WINDOW_CLOSED,
                event_origin=EventOrigin.WINDOW,
                window=self,
            )

            self.destroy()

    def on_render(self, event: Event) -> None:
        self.event_queue.tick()

        self.event_queue.fire(EventType.G_RENDER, event_origin=EventOrigin.WINDOW)

        self._render()

    def show(self) -> None:
        SDL_ShowWindow(self._window)
        self.shown = True

    def hide(self) -> None:
        SDL_HideWindow(self._window)
        self.shown = False

    def destroy(self) -> None:
        if self.destroyed:
            return
        self.destroyed = True

        SDL_DestroyRenderer(self._renderer)
        SDL_DestroyWindow(self._window)
