"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file for important information.
https://github.com/FluffyKn1ght/compygui
"""

from abc import abstractmethod, ABC

from sdl2 import SDL_INIT_VIDEO, SDL_Init
from sdl2.events import SDL_QUIT, SDL_Event, SDL_PollEvent

from compygui.errors import SDLErrorDetector
from compygui.misc import dummy
from compygui.window import Window
from compygui.decorators import must_be_initialized


class ComPyGUIApp(ABC):
    def __init__(
        self, *args, title: str = "ComPyGUI App", silence_license_info: bool = False
    ) -> None:
        if not silence_license_info:
            ComPyGUIApp._print_license_info()

        self.initialized: bool = False

        with SDLErrorDetector(error_info="Failed to initialize SDL2 library"):
            SDL_Init(SDL_INIT_VIDEO)

        self.title: str = title

        self.windows: list[Window] = []

        self.initialized = True

    @must_be_initialized
    def create_window(self, *args, **kwargs) -> Window:
        try:
            if kwargs["title"] == None:
                kwargs["title"] = self.title
        except KeyError:
            kwargs["title"] = self.title

        win: Window = Window(**kwargs)
        self.windows.append(win)

        return win

    @must_be_initialized
    def mainloop(self) -> None:
        # TODO: Add threading options?
        self._mainloop()

    @must_be_initialized
    def _mainloop(self) -> None:
        while True:
            event: SDL_Event = SDL_Event()
            with SDLErrorDetector(on_error=dummy):
                SDL_PollEvent(event)

                if event.type == SDL_QUIT:
                    break

    @staticmethod
    def _print_license_info() -> None:
        print(
            """
ComPyGUI library for Python 3.14+, version 0.1.0
(Copyright (C) 2026 FluffyKn1ght)
https://github.com/FluffyKn1ght/compygui

ComPyGUI is distributed under GPL v3, please see the
NOTICE and LICENSE files for more information
            """
        )

    @abstractmethod
    @must_be_initialized
    def run(self) -> None:
        pass
