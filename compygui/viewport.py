from compygui.component import Component


class Viewport(Component):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def destroy(self) -> None:
        pass
