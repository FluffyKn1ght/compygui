from enum import Enum
from typing import Any, Callable

from compygui.component import Component


class EventType:
    UNKNOWN: str = "?"

    APP_WINDOW_CLOSE: str = "app.window_close"

    WINDOW_WINDOW_CLOSED: str = "window.closed"


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
        event_origin: Component | EventOrigin = EventOrigin.UNKNOWN,
        event_oneshot: bool = False,
        **evdata
    ) -> None:
        self.type: str = type
        self.data: dict[str, Any] = evdata
        self.expires_in: int = event_expires_in
        self.origin: Component | EventOrigin = event_origin
        self.oneshot: bool = event_oneshot


class EventQueue:
    def __init__(self):
        self.events: list[Event] = []
        self._listeners: list[dict[str, Any]] = []

    def listen(
        self, for_event: str, condition: Callable[[Event], bool] | None = None
    ) -> Callable:
        def register_listener(func: Callable) -> Callable:
            def listen_wrapper(event: Event, *args, **kwargs) -> Any:
                return func(event)

            self._listeners.append(
                {"func": func, "type": for_event, "check": condition}
            )

            return listen_wrapper

        return register_listener

    def fire(self, evtype: str, *args, **evdata) -> None:
        event: Event = Event(evtype, *args, **evdata)
        self.events.append(event)  # TODO: Make events expire

        idx: int = 0
        for listener in self._listeners:
            if listener["type"] == event.type:
                if listener["check"] != None:
                    if not listener["check"](event):
                        continue

                listener["func"](event)

                if event.oneshot:
                    del self._listeners[idx]

            idx += 1
