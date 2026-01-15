"""
ComPyGUI - A competent Python GUI library
  Copyright (C) 2026  FluffyKn1ght

Please see the NOTICE file or compygui.compygui.ComPyGuiApp.NOTICE
for important license information.
https://github.com/FluffyKn1ght/compygui
"""

import uuid
from enum import Enum
from typing import Any, Callable

from compygui.component import Component
from compygui.errors import ComPyGUIError


class EventType:
    """Contains all Event() type strings in an easy-to-access place

    Should not be instantiated (will raise an error).
    """

    UNKNOWN: str = "?"

    G_RENDER: str = "render"

    APP_RENDER: str = "app.render"
    APP_WINDOW_CLOSE: str = "app.window_close"

    WINDOW_DESTROY: str = "window.destroy"

    GUI_CREATED: str = "gui.created"
    GUI_DESTROY: str = "gui.destroy"
    GUI_SIZE_CHANGED: str = "gui.size_changed"

    def __init__(self) -> None:
        raise NotImplemented("Can't instantiate EventType")


class EventOrigin(Enum):
    """Where did this Event() come from, if not from a Component()"""

    UNKNOWN = 0
    WINDOW = 1
    APP = 2
    OTHER = 255


class Event:
    """An application/component event

    Events are meant to solve the problem of calling-something-from-
    -somewhere-completely-unrelated, and also to allow (very limited)
    asyncrhonization. Events have a type string, origin (Component() or not),
    expiry time and age, and user-addable data (arguments).

    type: The type of the event
    event_expires_in: How many EventQueue() ticks does this event last
    event_origin: The origin of the event
    **evdata: Event data, stored in the Event().data property as a dict[str, Any]
    """

    def __init__(
        self,
        type: str,
        *args,
        event_expires_in: int = 1,
        event_origin: Component | EventOrigin,
        **evdata,
    ) -> None:
        self.type: str = type
        self.data: dict[str, Any] = evdata
        self.expires_in: int = event_expires_in
        self.origin: Component | EventOrigin = event_origin

        self.age: int = 0


class EventListener:
    """A structure that defines an event listener, as well as the rules and status of it

    Event listeners are more complicated than they seem: they have a
    target type, a callback, a condition/check function, a link to the
    class instance which created them and much more. This allows for
    complex, flexible event systems (including user events).

    callback: The function that will be called with an Event() once that Event() is fired
    type: The type of Event()s that this EventListener() listens to
    condition: An optional function that accepts an Event() and returns whether that event should be processed by the main callback
    oneshot: If True, then the EventListener() will self-destruct after one event
    disconnect: Which function to call then disconnecting this EventListener()
    instance: The class instance this EventListener() is linked to
    """

    def __init__(
        self,
        *args,
        callback: Callable[[Event]],
        type: str,
        condition: Callable[[Event], bool] | None = None,
        oneshot: bool,
        disconnect: Callable[[EventListener]],
        instance: Any,
    ) -> None:
        self.callback: Callable[[Event]] = callback
        self.type: str = type
        self.condition: Callable[[Event], bool] | None = condition
        self.oneshot: bool = oneshot
        self._disconnect: Callable[[EventListener]] = disconnect
        self.instance: Any = instance

        self.uuid: uuid.UUID = uuid.uuid4()
        self.valid: bool = True

    def __str__(self) -> str:
        return f"<compygui.events.EventListener for {self.type} at {hex(id(self))}: callback={self.callback} instance={self.instance} oneshot={self.oneshot} uuid={self.uuid} valid={self.valid}>"

    def disconnect(self) -> None:
        """Disconnects this EventListener(), making it no longer react to any events"""

        if self.oneshot and not self.valid:
            return

        self._disconnect(self)
        self.valid = False


class EventQueue:
    """An event queue that handles listener connection/disconnection"""

    def __init__(self):
        self.events: list[Event] = []
        self._listeners: list[EventListener] = []

    def connect(
        self,
        instance: Any,
        callback: Callable[[Event]],
        for_event: str,
        *args,
        condition: Callable[[Event], bool] | None = None,
        oneshot: bool = False,
    ) -> EventListener:
        """Creates and connects an EventListener() to this EventQueue()

        instance: The class instance the EventListener() will be linked to
        callback: The function that will be called with an Event() once that Event() is fired
        for_event: The type of Event()s that this EventListener() will listen to
        condition: An optional function that accepts an Event() and returns whether that event
            should be processed by the main callback
        oneshot: If True, then the EventListener() will self-destruct after one event
        """

        listener: EventListener = EventListener(
            callback=callback,
            type=for_event,
            condition=condition,
            oneshot=oneshot,
            disconnect=self.disconnect,
            instance=instance,
        )
        self._listeners.append(listener)
        return listener

    def fire(
        self, evtype: str, *args, event_origin: Component | EventOrigin, **evdata
    ) -> None:
        """Creates an "fires" an event, triggering the appropriate listeners and
        adding it to the event queue.

        evtype: The type of the event to fire
        event_origin: The origin of the event
        **evdata: Any other kwargs that will get interpreted as event data (arguments)
        """

        if len(self.events) >= 1024:
            raise OverflowError("Event queue size limit reached (1024 events)")

        if len(self._listeners) >= 1024:
            raise OverflowError(
                "Event listener array size limit reached (1024 event listeners)"
            )

        event: Event = Event(evtype, *args, **evdata, event_origin=event_origin)
        self.events.append(event)

        for listener in self._listeners:
            if listener.type == event.type:
                if listener.condition:
                    if not listener.condition(event):
                        continue

                if not listener.valid:
                    raise ComPyGUIError(
                        f"[ComPyGUI BUG] Invalid (disconnected) listener in EventQueue()._listeners at index {self._listeners.index(listener)}"
                    )

                listener.callback(event)

                if listener.oneshot:
                    listener.disconnect()

    def disconnect(self, listener_or_uuid: EventListener | uuid.UUID) -> None:
        """Disconnects an EventListener() from this EventQueue()"""

        listener: EventListener | None = None
        if isinstance(listener_or_uuid, EventListener):
            listener = listener_or_uuid
        elif isinstance(listener_or_uuid, uuid.UUID):
            for lis in self._listeners:
                if lis.uuid == listener_or_uuid:
                    listener = lis

        if listener is None:
            raise ValueError(f"Unable to find listener from UUID {listener_or_uuid}")

        if not listener.valid and not listener in self._listeners:
            raise ValueError(f"Listener {listener} has already been disconnected")

        self._listeners.remove(listener)

    def tick(self) -> None:
        """Updates the ages of all events in the queue and clears out the expired oness"""

        for event in self.events:
            event.age += 1

            if event.age >= event.expires_in:
                self.events.remove(event)
