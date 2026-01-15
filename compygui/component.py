"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

from abc import ABC


class Component(ABC):
    """An abstract base class for a Component - the minimal ComPyGUI object.

    A Component is an object that has one parent and any number of children,
    which define its location in a virtual tree, known as the VCT (Virtual
    Component Tree). The BaseComponent is the most bare-bones type of component,
    as it's meant to serve as a base for other component types (however, you
    shouldn't have a reason to use anything besides Component() and GUIComponent()).

    *children: The children of the component
    """

    def __init__(self, *children) -> None:
        self.destroyed: bool = False

        self._parent: Component | None = None
        self._children: list[Component] = []

        for child in children:
            if type(child) is Component:
                child.reparent(self)

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

    def _add_child(self, child: Component) -> None:
        self._children.append(child)
        self.add_child(child)

    def add_child(self, child: Component) -> None:
        pass

    def reparent(self, to: Component | None) -> None:
        """Reparent this Component() to another Component()"""

        # TODO: Events
        if self._parent:
            try:
                self._parent.children.remove(self)
            except ValueError:
                pass

        self._parent = to

        if self._parent:
            self._parent._add_child(self)

    def destroy(self) -> None:
        """Cleans up and deletes the Component()"""
        pass
