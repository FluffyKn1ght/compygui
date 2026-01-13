from abc import ABC, abstractmethod


class BaseComponent(ABC):
    """An abstract base class for a Component - the minimal ComPyGUI object.

    A Component is an object that has one parent and any number of children,
    which define its location in a virtual tree, known as the VCT (Virtual
    Component Tree).
    """

    def __init__(self) -> None:
        self._parent: BaseComponent | None = None
        self._children: list[BaseComponent] = []

    def __del__(self) -> None:
        self.destroy()

    @property
    def parent(self) -> BaseComponent | None:
        return self._parent

    @parent.setter
    def parent(self) -> None:
        raise AttributeError(
            "Unable to set BaseComponent().parent directly - use BaseComponent.reparent() instead"
        )

    @property
    def children(self) -> list[BaseComponent]:
        return self._children

    @children.setter
    def children(self) -> None:
        raise AttributeError(
            "Unable to set BaseComponent().children directly - use BaseComponent.reparent() on the child component instead"
        )

    def reparent(self, to: BaseComponent | None) -> None:
        """Reparent another BaseComponent() to this BaseComponent()"""

        # TODO: Events
        if self._parent:
            try:
                self._parent.children.remove(self)
            except ValueError:
                pass

        self._parent = to
        if self._parent:
            if self in self._parent.children:
                self._parent.children.append(self)

    @abstractmethod
    def destroy(self) -> None:
        """Clean up and delete this component"""
        pass
