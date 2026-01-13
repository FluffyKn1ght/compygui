from compygui.basecomponent import BaseComponent
from compygui.compygui import ComPyGUIApp
from compygui.window import Window


class Component(BaseComponent):
    """A component that is tied to a Window() of a ComPyGUIApp()"""

    def __init__(self) -> None:
        super().__init__()

        self.window: Window | None = None
        self._app: ComPyGUIApp | None = None

    @property
    def app(self) -> ComPyGUIApp:
        if self._app:
            return self._app
        else:
            raise ValueError("No app assigned to Component()")

    @app.setter
    def app(self, to: ComPyGUIApp) -> None:
        if not self._app:
            self._app = to
        else:
            raise ValueError("Already assigned app to Component()")
