"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from compygui import ComPyGUIApp, Window
from compygui.datatypes import Vector2
from compygui.window import WindowPositionFlags


class BlankWindowApp(ComPyGUIApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def setup(self):
        window: Window = self.create_window(
            position=WindowPositionFlags.centered(), size=Vector2(720, 540)
        )
        window.show()


app: BlankWindowApp = BlankWindowApp(title="Blank Window")

app.run()

app.quit()
