"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from abc import abstractmethod, ABC

from sdl2 import SDL_INIT_VIDEO, SDL_Init, SDL_Quit
from sdl2.events import SDL_QUIT, SDL_Event, SDL_PollEvent

from compygui.errors import SDLErrorDetector
from compygui.misc import dummy
from compygui.window import Window


class ComPyGUIApp(ABC):
    """Abstract base class for a ComPyGUI app"""

    NOTICE: str = """
ComPyGUI - A competent GUI library for Python
Copyright (C) 2026 FluffyKn1ght

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program in the form of a LICENSE file. If not,
please see <https://www.gnu.org/licenses/>.
    """

    def __init__(
        self, *args, title: str = "ComPyGUI App", silence_license_info: bool = False
    ) -> None:
        self.destroyed: bool = False

        if not silence_license_info:
            ComPyGUIApp._print_license_info()

        with SDLErrorDetector(error_info="Failed to initialize SDL2 library"):
            SDL_Init(SDL_INIT_VIDEO)

        self.title: str = title

        self.windows: list[Window] = []

    def __del__(self):
        self.quit()

    def _mainloop(self) -> None:
        """Starts the main application loop"""
        while True:
            event: SDL_Event = SDL_Event()
            with SDLErrorDetector(on_error=dummy):
                SDL_PollEvent(event)

                if event.type == SDL_QUIT:
                    break

    def create_window(self, *args, **kwargs) -> Window:
        """Creates and registers a Window to this app

        **kwargs: Window.__init__() keyword arguments
        """
        try:
            if not kwargs["title"]:
                kwargs["title"] = self.title
        except KeyError:
            kwargs["title"] = self.title

        win: Window = Window(*args, **kwargs)
        self.register_window(win)

        return win

    def register_window(self, window: Window) -> None:
        """Registers a window to this app

        window: The Window() to register
        """

        # TODO: Register a renderer
        self.windows.append(window)

    def quit(self) -> None:
        """Clean up and close the app"""
        if self.destroyed:
            return

        win_idx: int = 0
        for window in self.windows:
            window.destroy()
            del self.windows[win_idx]
            win_idx += 1

        SDL_Quit()

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
    def setup(self) -> None:
        """(Abstract method) Sets up the app"""
        pass

    def run(self) -> None:
        """(Abstract method) Launches the app."""
        self.setup()
        self._mainloop()
