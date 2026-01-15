from enum import Enum
from typing import Any, Callable

from compygui.component import Component


class EventType:
    UNKNOWN: str = "?"

    G_RENDER: str = "render"

    APP_RENDER: str = "app.render"
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
        **evdata
    ) -> None:
        self.type: str = type
        self.data: dict[str, Any] = evdata
        self.expires_in: int = event_expires_in
        self.origin: Component | EventOrigin = event_origin


class EventQueue:
    def __init__(self):
        self.events: list[Event] = []
        self._listeners: list[dict[str, Any]] = []

    def listen(
        self,
        for_event: str,
        condition: Callable[[Event], bool] | None = None,
        *args,
        oneshot: bool = False
    ) -> Callable:
        def register_listener(func: Callable) -> Callable:
            def listen_wrapper(event: Event, *args, **kwargs) -> Any:
                return func(event)

            self._listeners.append(
                {
                    "func": func,
                    "type": for_event,
                    "check": condition,
                    "oneshot": oneshot,
                }
            )

            return listen_wrapper

        return register_listener

    def fire(self, evtype: str, *args, **evdata) -> None:
        if len(self.events) >= 1024:
            raise OverflowError("Event queue size limit reached (1024 events)")

        if len(self._listeners) >= 1024:
            raise OverflowError(
                "Event listener array size limit reached (1024 event listeners)"
            )

        event: Event = Event(evtype, *args, **evdata)
        self.events.append(event)  # TODO: Make events expire

        idx: int = -1
        for listener in self._listeners:
            idx += 1
            if listener["type"] == event.type:
                if listener["check"] != None:
                    if not listener["check"](event):
                        continue

                listener["func"](event)

                if listener["oneshot"]:
                    del self._listeners[idx]
