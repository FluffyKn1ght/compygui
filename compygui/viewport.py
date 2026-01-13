from abc import ABC, abstractmethod
from dataclasses import dataclass
from sdl2.surface import (
    SDL_CreateRGBSurface,
    SDL_FillRect,
    SDL_FreeSurface,
    SDL_Surface,
)
from compygui.component import Component
from compygui.datatypes import IRect2, RGBAColor, IVector2
from compygui.errors import ComPyGUIError, SDLErrorDetector


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
        *args,
        size: IVector2,
        mask: RGBAColor = RGBAColor.WHITE(),
        bit_depth: int = 8,
        bg_color: RGBAColor = RGBAColor.TWHITE(),
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self._surface: SDL_Surface | None = None

        self.size: IVector2 = size
        self.bit_depth: int = bit_depth
        self.mask: RGBAColor = mask

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
        super().destroy()

    @abstractmethod
    def render(self) -> None:
        """Re-render the BaseViewport() and all of its GUIComponent()s"""
        pass


class Viewport(BaseViewport):
    """A viewport that renders its child Component()s onto its _surface

    Inherited from BaseViewport:
        size: The starting size of the Viewport()
        mask: The color mask/pixel format of the Viewport()'s _surface
        bit_depth: The bit depth of the Viewport()'s _surface

    bg_color: The color used for filling the background at the start
        of a re-render.
    """

    def __init__(
        self, *args, bg_color: RGBAColor = RGBAColor.TBLACK(), **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.bg_color: RGBAColor = bg_color

    def render(self) -> None:
        if self.destroyed:
            return

        if not self._surface:
            raise ComPyGUIError("Viewport doesn't have a _surface")

        with SDLErrorDetector("Viewport rendering failed"):
            SDL_FillRect(
                self._surface,
                self.get_rect().as_sdl_rect(),
                self.bg_color.as_int(min(self.bit_depth, 8)),
            )
