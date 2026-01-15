from sdl2.surface import SDL_FillRect, SDL_Surface
from compygui.datatypes.rect2 import IRect2
from compygui.datatypes.rgba import RGBAColor, RGBAMask
from compygui.datatypes.vector2 import IVector2
from compygui.events import EventQueue
from compygui.guicomponent import GUIComponent


class GUIColorRectangle(GUIComponent):
    def __init__(self, *children, size: IVector2, color: RGBAColor, **kwargs) -> None:
        super().__init__(*children, **kwargs)

        self.size: IVector2 = size
        self.color: RGBAColor = color

    def calculate(self, delta: int) -> IVector2:
        return self.size

    def render(self, delta: int, to: SDL_Surface) -> None:
        SDL_FillRect(
            to,
            IRect2.from_vectors(self.position, self.calcd_size).as_sdl_rect(),
            self.color.as_int(8),
        )
