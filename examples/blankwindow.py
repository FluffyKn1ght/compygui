"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file for important information.
https://github.com/FluffyKn1ght/compygui
"""

from compygui import ComPyGUIApp, Window
from compygui.datatypes import Vector2
from compygui.window import WindowPositionFlags


class BlankWindowApp(ComPyGUIApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def run(self):
        win: Window = self.create_window(
            position=WindowPositionFlags.centered(), size=Vector2(512, 384)
        )
        self.mainloop()


app: BlankWindowApp = BlankWindowApp(title="Blank Window")

app.run()
