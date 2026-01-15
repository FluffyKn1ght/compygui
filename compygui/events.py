import warnings
import uuid
from enum import Enum
from typing import Any, Callable

from compygui.component import Component


class EventType:
    UNKNOWN: str = "?"

    G_RENDER: str = "render"

    APP_RENDER: str = "app.render"
    APP_WINDOW_CLOSE: str = "app.window_close"

    WINDOW_DESTROY: str = "window.destroy"


class EventOrigin(Enum):
    UNKNOWN = 0
    WINDOW = 1
    APP = 2
    OTHER = 255


class Event:
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
    def __init__(
        self,
        *args,
        callback: Callable[[Event]],
        type: str,
        condition: Callable[[Event], bool] | None,
        oneshot: bool,
        disconnect: Callable[[EventListener]],
        instance: Any,
    ) -> None:
        self.callback: Callable[[Event]] = callback
        self.condition: Callable[[Event], bool] | None = condition
        self.type: str = type
        self.oneshot: bool = oneshot
        self._disconnect: Callable[[EventListener]] = disconnect
        self.instance: Any = instance

        self.uuid: uuid.UUID = uuid.uuid4()
        self.valid: bool = True

    def __str__(self) -> str:
        return f"<compygui.events.EventListener for {self.type} at {hex(id(self))}: callback={self.callback} condition={self.condition} instance={self.instance} oneshot={self.oneshot} uuid={self.uuid} valid={self.valid}>"

    def disconnect(self) -> None:
        if self.oneshot and not self.valid:
            return

        self._disconnect(self)
        self.valid = False


class EventQueue:
    def __init__(self):
        self.events: list[Event] = []
        self._listeners: list[EventListener] = []

    def connect(
        self,
        instance: Any,
        callback: Callable[[Event]],
        for_event: str,
        condition: Callable[[Event], bool] | None = None,
        *args,
        oneshot: bool = False,
    ) -> EventListener:
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
                if listener.condition != None:
                    if not listener.condition(event):
                        continue

                if not listener.valid:
                    raise ValueError(
                        f"[ComPyGUI BUG] Invalid (disconnected) listener in EventQueue()._listeners at index {self._listeners.index(listener)}"
                    )

                listener.callback(event)

                if listener.oneshot:
                    listener.disconnect()

    def disconnect(self, listener_or_uuid: EventListener | uuid.UUID) -> None:
        listener: EventListener | None = None
        if type(listener_or_uuid) is EventListener:
            listener = listener_or_uuid
        elif type(listener_or_uuid) is uuid.UUID:
            for lis in self._listeners:
                if lis.uuid == listener_or_uuid:
                    listener = lis

        if listener is None:
            raise ValueError(f"Unable to find listener from UUID {listener_or_uuid}")

        if not listener.valid and not listener in self._listeners:
            raise ValueError(f"Listener {listener} has already been disconnected")

        self._listeners.remove(listener)

    def tick(self) -> None:
        for event in self.events:
            event.age += 1

            if event.age >= event.expires_in:
                self.events.remove(event)
