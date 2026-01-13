from compygui.component import Component
from compygui.compygui import ComPyGUIApp
from compygui.window import Window


class Viewport(Component):
    def __init__(self, *args, window: Window, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.window = window

    def destroy(self) -> None:
        pass
