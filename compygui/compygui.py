"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from abc import abstractmethod, ABC
import time

from sdl2 import SDL_INIT_VIDEO, SDL_Init, SDL_Quit
from sdl2.events import (
    SDL_QUIT,
    SDL_WINDOWEVENT,
    SDL_Event,
    SDL_PollEvent,
    SDL_WindowEvent,
)
from sdl2.video import SDL_WINDOWEVENT_CLOSE, SDL_GetWindowID, SDL_GetWindowTitle

from compygui.errors import ComPyGUIError, SDLErrorDetector
from compygui.events import Event, EventOrigin, EventQueue, EventType
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
        self,
        *args,
        title: str = "ComPyGUI App",
        silence_license_info: bool = False,
        framerate: int = 60,
    ) -> None:
        self.destroyed: bool = False

        if not silence_license_info:
            ComPyGUIApp._print_license_info()

        with SDLErrorDetector(error_info="Failed to initialize SDL2 library"):
            SDL_Init(SDL_INIT_VIDEO)

        self.title: str = title
        self.framerate: int = framerate

        self.windows: list[Window] = []
        self.running: bool = False
        self.event_queue = EventQueue()

        self._last_frame_time: float = time.thread_time()

        self.event_queue.connect(self, self.on_window_destroy, EventType.WINDOW_DESTROY)

    def __del__(self):
        self.quit()

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

    def _mainloop(self) -> None:
        while self.running:
            event = SDL_Event()
            with SDLErrorDetector(on_error=dummy):
                SDL_PollEvent(event)

                if event.type == SDL_WINDOWEVENT:
                    if event.window.event == SDL_WINDOWEVENT_CLOSE:
                        self.event_queue.fire(
                            EventType.APP_WINDOW_CLOSE,
                            event_origin=EventOrigin.APP,
                            window_id=event.window.windowID,
                        )

            curtime: float = time.thread_time()
            self.event_queue.fire(
                EventType.APP_RENDER,
                event_origin=EventOrigin.APP,
                delta=curtime - self._last_frame_time,
            )

            self._last_frame_time = curtime

            self.event_queue.tick()

    def _get_window_by_id(self, id: int) -> Window | None:
        """Gets a Window from a window ID

        id: The id of the window to return
        """

        for win in self.windows:
            if id == SDL_GetWindowID(win._window):
                return win

        return None

    def create_window(self, *args, **kwargs) -> Window:
        """Creates and registers a Window() to this app

        **kwargs: Window.__init__() keyword arguments
        """
        try:
            if not kwargs["title"]:
                kwargs["title"] = self.title
        except KeyError:
            kwargs["title"] = self.title

        win: Window = Window(*args, app_event_queue=self.event_queue, **kwargs)
        self.register_window(win)

        return win

    def register_window(self, window: Window) -> None:
        """Registers a window to this app

        window: The Window() to register
        """

        idx: int = len(self.windows) - 1
        self.windows.append(window)

    def on_window_destroy(self, event: Event) -> None:
        self.windows.remove(event.data["window"])

        if not self.windows:
            self.running = False

    def run(self) -> None:
        """Launches the app."""
        if self.running:
            raise ComPyGUIError("App is already running")
        self.setup()
        self.running = True
        self._mainloop()

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

    @abstractmethod
    def setup(self) -> None:
        """(Abstract method) Sets up the app"""
        pass
