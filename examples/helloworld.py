"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

"""Hello World

A simple ComPyGUI demo project.
"""

from compygui import ComPyGUIApp, Window
from compygui.datatypes.rgba import RGBAColor
from compygui.datatypes.vector2 import IVector2, Vector2
from compygui.gui.colorrect import GUIColorRectangle
from compygui.guicomponent import GUIComponent
from compygui.viewport import Viewport
from compygui.window import WindowPositionFlags


def hello_world_layout() -> GUIComponent:
    return GUIColorRectangle(
        position=IVector2(360, 270),
        size=Vector2(1, 0.8),
        color=RGBAColor.WHITE(),
        anchor_point=Vector2(0.5, 0.5),
    )


class HelloWorldApp(ComPyGUIApp):
    """Main app class"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def setup(self):
        window: Window = self.create_window(
            position=WindowPositionFlags.centered(),
            size=IVector2(720, 540),
        )
        hello_world_layout().reparent(window.viewport)
        window.show()


app: HelloWorldApp = HelloWorldApp(title="Hello, ComPyGUI! :D")

app.run()

app.quit()
