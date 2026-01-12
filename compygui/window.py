"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file for important information.
https://github.com/FluffyKn1ght/compygui
"""

from sdl2 import SDL_WINDOW_RESIZABLE, SDL_CreateWindow, SDL_HideWindow, SDL_WindowFlags
from sdl2.video import (
    SDL_WINDOWPOS_CENTERED,
    SDL_WINDOWPOS_UNDEFINED,
    SDL_ShowWindow,
    SDL_Window,
)
from compygui.datatypes import Vector2
from compygui.errors import SDLErrorDetector
from compygui.decorators import must_be_initialized


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


class Window:
    def __init__(
        self,
        *args,
        title="Window",
        position: Vector2 | WindowPositionFlags,
        size: Vector2,
        flags: int = SDL_WINDOW_RESIZABLE
    ) -> None:
        self.initialized: bool = False

        self._window: SDL_Window | None = None
        self.shown: bool = False

        with SDLErrorDetector(error_info="Failed to create window"):
            self._window = SDL_CreateWindow(
                bytes(title, encoding="utf-8"),
                position.x,
                position.y,
                size.x,
                size.y,
                flags,
            )

        self.initialized = True

    @must_be_initialized
    def show(self) -> None:
        SDL_ShowWindow(self._window)

    @must_be_initialized
    def hide(self) -> None:
        SDL_HideWindow(self._window)
