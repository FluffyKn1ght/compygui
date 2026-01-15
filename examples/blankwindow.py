"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

"""Blank Window

Creates a completely blank window. Good template/boilerplate project.
"""

from compygui import ComPyGUIApp, Window
from compygui.datatypes.vector2 import IVector2
from compygui.window import WindowPositionFlags


class BlankWindowApp(ComPyGUIApp):
    """Main app class"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def setup(self):
        window: Window = self.create_window(
            position=WindowPositionFlags.centered(), size=IVector2(720, 540)
        )
        window.show()


app: BlankWindowApp = BlankWindowApp(title="Blank Window")

app.run()

app.quit()
