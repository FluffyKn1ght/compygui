from sdl2.surface import SDL_FillRect, SDL_Surface
from compygui.datatypes.rect2 import IRect2
from compygui.datatypes.rgba import RGBAColor
from compygui.datatypes.vector2 import IVector2, Vector2
from compygui.guicomponent import GUIComponent


class GUIColorRectangle(GUIComponent):
    def __init__(
        self, *children, size: IVector2 | Vector2, color: RGBAColor, **kwargs
    ) -> None:
        super().__init__(*children, **kwargs)

        self.size: IVector2
        self._relsize: Vector2 | None = None

        if isinstance(size, IVector2):
            self.size = size
        elif isinstance(size, Vector2):
            self._relsize = size

        self.color: RGBAColor = color

    def setup(self) -> None:
        if self._relsize:
            self.size = (self._relsize * self.get_viewport_size()).rounded()

    def calculate(self, delta: int) -> IVector2:
        return self.size

    def render(self, delta: int, to: SDL_Surface) -> None:
        SDL_FillRect(
            to,
            IRect2.from_vectors(self.topleft, self.calcd_size).as_sdl_rect(),
            self.color.as_int(8),
        )
