"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Vector2:
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.x: int = x
        self.y: int = y

    def __or__(self, value: Any) -> Vector2:
        if type(value) is Vector2:
            return Vector2(
                self.x if self.x != 0 else value.x, self.y if self.y != 0 else value.y
            )
        else:
            raise ValueError(
                f"Can't {'"|"'} a Vector2 and {type(value).__name__} together "
            )

    @staticmethod
    def ZERO() -> Vector2:
        return Vector2(0, 0)

    @staticmethod
    def ONE() -> Vector2:
        return Vector2(1, 1)

    @staticmethod
    def UP() -> Vector2:
        return Vector2(0, -1)

    @staticmethod
    def DOWN() -> Vector2:
        return Vector2(0, 1)

    @staticmethod
    def LEFT() -> Vector2:
        return Vector2(-1, 0)

    @staticmethod
    def RIGHT() -> Vector2:
        return Vector2(1, 0)


@dataclass
class Rect2:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        super().__init__()
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h

    # TODO: Implement methods like in Vector2
