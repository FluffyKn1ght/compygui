from abc import ABC, abstractmethod
from dataclasses import dataclass
from sdl2.surface import (
    SDL_CreateRGBSurface,
    SDL_FillRect,
    SDL_FreeSurface,
    SDL_Surface,
)
from compygui.component import Component
from compygui.datatypes.rect2 import IRect2
from compygui.datatypes.vector2 import IVector2
from compygui.datatypes.rgba import RGBAColor, RGBAMask
from compygui.errors import ComPyGUIError, SDLErrorDetector
from compygui.events import Event, EventListener, EventQueue, EventType


class BaseViewport(Component, ABC):
    """An abstract base class for an RGBA surface that can render any content.

    This is the top-level VCT node. All GUIComponents have to be parented
    to a BaseViewport() (or, better, the non-abstract Viewport()) to recieve
    events from ComPyGUIApp() and Window() objects and actually get rendered.

    size: The starting size of the Viewport()
    mask: The color mask/pixel format of the Viewport()'s _surface
    bit_depth: The bit depth of the Viewport()'s _surface
    """

    def __init__(
        self,
        *children,
        size: IVector2,
        mask: RGBAMask = RGBAMask.RGBA(),
        bit_depth: int = 32,
        window_events: EventQueue,
        **props
    ) -> None:
        super().__init__(*children, **props)

        self._surface: SDL_Surface | None = None
        self.size: IVector2 = size
        self.bit_depth: int = bit_depth
        self.mask: RGBAMask = mask

        self.window_events: EventQueue = window_events

        self._render_listener: EventListener = self.window_events.connect(
            self, self._on_render, EventType.G_RENDER
        )

        self.recreate_surface()

    def _on_render(self, event: Event) -> None:
        self.render()

    def recreate_surface(self) -> None:
        """(re-)Create the Viewport()'s surface to match class properties"""

        with SDLErrorDetector(error_info="Failed to (re)create viewport surface"):
            if self._surface:
                SDL_FreeSurface(self._surface)
                self._surface = None

            self._surface = SDL_CreateRGBSurface(
                0,
                self.size.x,
                self.size.y,
                self.bit_depth,
                self.mask.r,
                self.mask.g,
                self.mask.b,
                self.mask.a,
            )

    def get_rect(self) -> IRect2:
        return IRect2.from_vectors(IVector2.ZERO(), self.size)

    def destroy(self) -> None:
        """Clean up and delete the BaseViewport()"""
        if self._surface:
            SDL_FreeSurface(self._surface)
        self._render_listener.disconnect()
        super().destroy()

    @abstractmethod
    def render(self) -> None:
        """Re-render the BaseViewport() and all of its GUIComponent()s"""
        pass


class Viewport(BaseViewport):
    """A viewport that renders its child Component()s onto its _surface

    bg_color: The color used for filling the background at the start
        of a re-render.
    """

    def __init__(
        self, *children, bg_color: RGBAColor = RGBAColor.TBLACK(), **props
    ) -> None:
        super().__init__(*children, **props)

        self.bg_color: RGBAColor = bg_color

    def render(self) -> None:
        """Renders the contents of this Viewport() to its _surface"""

        if self.destroyed:
            return

        if not self._surface:
            raise ComPyGUIError("Viewport() doesn't have a _surface")

        with SDLErrorDetector("Viewport rendering failed"):
            SDL_FillRect(
                self._surface,
                self.get_rect().as_sdl_rect(),
                self.bg_color.as_int(8),
            )
