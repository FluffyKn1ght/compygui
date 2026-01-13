from abc import ABC, abstractmethod

from compygui.window import Window


class Component(ABC):
    """An abstract base class for a Component - the minimal ComPyGUI object.

    A Component is an object that has one parent and any number of children,
    which define its location in a virtual tree, known as the VCT (Virtual
    Component Tree). The BaseComponent is the most bare-bones type of component,
    as it's meant to serve as a base for other component types (however, you
    shouldn't have a reason to use anything besides Component() and GUIComponent()).
    """

    def __init__(self) -> None:
        self.destroyed: bool = False

        self._parent: Component | None = None
        self._children: list[Component] = []

    def __del__(self) -> None:
        self.destroy()

    @property
    def parent(self) -> Component | None:
        return self._parent

    @parent.setter
    def parent(self) -> None:
        raise AttributeError(
            "Unable to set Component().parent directly - use Component.reparent() instead"
        )

    @property
    def children(self) -> list[Component]:
        return self._children

    @children.setter
    def children(self) -> None:
        raise AttributeError(
            "Unable to set Component().children directly - use Component.reparent() on the child component instead"
        )

    def reparent(self, to: Component | None) -> None:
        """Reparent another Component() to this Component()"""

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

    def destroy(self) -> None:
        """Clean up and delete this component"""
        pass
