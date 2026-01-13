"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from enum import Enum
from typing import Callable

from sdl2.error import SDL_ClearError, SDL_GetError


class ClearErrorOn(Enum):
    """When should an SDLErrorHandler() run SDL_ClearError()"""

    NEVER = 0b00
    ENTER = 0b01
    EXIT = 0b10
    ENTER_EXIT = ENTER | EXIT


class SDLError(Exception):
    """SDL2-related error"""

    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg: str = msg

    @staticmethod
    def from_sdl_geterror(info: str) -> SDLError:
        return SDLError(f"{info}: SDL error: {SDL_GetError().decode("utf-8")}")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.msg}"


class SDLErrorDetector:
    """A context manager that can be used to check for any
    SDL_GetError() errors and raise them as SDLError-s
    """

    def __init__(
        self,
        *args,
        on_error: Callable[[SDLError]] | None = None,
        error_info: str = "An SDL error has occured:",
        clear_error_on: ClearErrorOn = ClearErrorOn.ENTER_EXIT,
    ) -> None:
        self.on_error: Callable[[SDLError]] = SDLErrorDetector._raise_sdlerror
        if on_error:
            self.on_error = on_error

        self.error_info: str = error_info
        self.clear_error_on: ClearErrorOn = clear_error_on

    def __enter__(self) -> None:
        if self.clear_error_on.value & ClearErrorOn.ENTER.value:
            SDL_ClearError()

    def __exit__(self, *args) -> None:
        if SDL_GetError():
            self.on_error(SDLError.from_sdl_geterror(self.error_info))

        if self.clear_error_on.value & ClearErrorOn.EXIT.value:
            SDL_ClearError()

    @staticmethod
    def _raise_sdlerror(e: SDLError) -> None:
        """Default on_error method. Raises an SDLError for handling via a try/except"""
        raise e


class ComPyGUIError(Exception):
    """ComPyGUI-related error"""

    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg: str = msg

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.msg}"
