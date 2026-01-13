from ast import Call
from enum import Enum
from typing import Any, Callable

from compygui.component import Component


class EventType(Enum):
    UNKNOWN = 0
    WINDOW_CLOSE = 1
    WINDOW_CLOSED = 2

    def __call__(self, *args, **kwargs):
        pass


class EventOrigin(Enum):
    UNKNOWN = 0
    WINDOW = 1
    APP = 2
    OTHER = 255


class Event:
    def __init__(
        self,
        type: EventType,
        *args,
        event_expires_in: int = 1,
        event_origin: Component | EventOrigin = EventOrigin.UNKNOWN,
        event_oneshot: bool = False,
        **evdata
    ) -> None:
        self.type: EventType = type
        self.data: dict[str, Any] = evdata
        self.expires_in: int = event_expires_in
        self.origin: Component | EventOrigin = event_origin
        self.oneshot: bool = event_oneshot


class EventQueue:
    def __init__(self):
        self.events: list[Event] = []
        self._listeners: list[dict[str, Callable[[Event]] | EventType]] = []

    def listen(self, for_event: EventType) -> Callable:
        def listen_deco(func: Callable) -> Callable:
            def listen_wrapper(event: Event, *args, **kwargs) -> Any:
                return func(event)

            self._listeners.append({"func": func, "type": for_event})

            return listen_wrapper

        return listen_deco

    def fire(self, evtype: EventType, *args, **evdata) -> None:
        event: Event = Event(evtype, *args, **evdata)
        self.events.append(event)  # TODO: Make events expire

        idx: int = 0
        for listener in self._listeners:
            if listener["type"] == event.type:
                listener["func"](event)

                if event.oneshot:
                    del self._listeners[idx]

            idx += 1
