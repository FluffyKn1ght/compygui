"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from typing import Callable

from compygui.errors import NotInitializedError


def must_be_initialized(func: Callable) -> Callable:
    def must_be_initialized_wrapper(self, *args, **kwargs):
        if self.initialized:
            func(self, *args, **kwargs)
        else:
            raise NotInitializedError()

    return must_be_initialized_wrapper
