"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from abc import ABC, abstractmethod
from enum import Enum
from types import NoneType
from typing import Any

from sdl2.surface import (
    SDL_BlitSurface,
    SDL_CreateRGBSurface,
    SDL_FreeSurface,
    SDL_Surface,
)
from compygui.component import Component
from compygui.datatypes.rect2 import IRect2
from compygui.datatypes.rgba import RGBAMask
from compygui.datatypes.vector2 import IVector2, Vector2
from compygui.errors import ComPyGUIError, SDLErrorDetector
from compygui.events import Event, EventListener, EventOrigin, EventQueue, EventType


class GUIComponent(Component):
    def __init__(
        self,
        *children,
        _rgba_mask: RGBAMask = RGBAMask.RGBA(),
        _bit_depth: int = 32,
        position: IVector2,
        anchor_point: Vector2 = Vector2.ZERO(),
    ) -> None:
        super().__init__(*children)

        self._surface: SDL_Surface | None = None
        self._rgba_mask: RGBAMask = _rgba_mask
        self._bit_depth: int = _bit_depth

        self._calculated_size: IVector2 = IVector2.ZERO()

        self.tree_events: EventQueue

        self.position: IVector2 = position
        self.anchor_point: Vector2 = anchor_point

        self._recreate_surface(self.calcd_size)

        self.render_listener: EventListener

    @property
    def topleft(self) -> IVector2:
        return self.position - (self.anchor_point * self.calcd_size).rounded()

    @property
    def calcd_size(self) -> IVector2:
        return self._calculated_size

    @calcd_size.setter
    def calcd_size(self, _to: IVector2) -> None:
        raise NotImplemented(
            "Can't set the calculated rectangle of a GUIComponent() directly"
        )

    def _setup(self, tree_ev: EventQueue) -> None:
        self.tree_events = tree_ev
        self.tree_events.fire(EventType.GUI_CREATED, event_origin=self)

        self.render_listener = self.tree_events.connect(
            self, self._render, EventType.G_RENDER
        )

        self.setup()

    def _recreate_surface(self, size: IVector2) -> None:
        with SDLErrorDetector("Could not (re-)create GUIComponent surface"):
            if self._surface:
                SDL_FreeSurface(self._surface)
                self._surface = None

            self._surface = SDL_CreateRGBSurface(
                0,
                size.x,
                size.y,
                self._bit_depth,
                self._rgba_mask.r,
                self._rgba_mask.g,
                self._rgba_mask.b,
                self._rgba_mask.a,
            )

    def _render(self, event: Event) -> None:
        new_calcd_size: IVector2 = self.calculate(event.data["delta"])
        if new_calcd_size != self._calculated_size:
            self._recreate_surface(new_calcd_size)
            self.tree_events.fire(
                EventType.GUI_SIZE_CHANGED,
                event_origin=self,
                old=self._calculated_size,
                new=new_calcd_size,
            )
        self._calculated_size = new_calcd_size

        if not self._surface:
            raise ComPyGUIError("GUIComponent() has no _surface")

        for child in self.children:
            if isinstance(child, GUIComponent):
                child.render(event.data["delta"], self._surface)

        with SDLErrorDetector("Failed to render GUIComponent"):
            self.render(event.data["delta"], self._surface)

    def setup(self) -> None:
        pass

    def render(self, delta: int, to: SDL_Surface) -> None:
        SDL_BlitSurface(
            self._surface, None, to, IRect2.from_vectors(self.position, self.calcd_size)
        )

    def calculate(self, delta: int) -> IVector2:
        return IVector2.ZERO()

    def destroy(self) -> None:
        self.tree_events.fire(EventType.GUI_DESTROY, event_origin=self)
        self.render_listener.disconnect()
        super().destroy()
