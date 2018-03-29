from enum import Enum


class EventKind(Enum):
    ENTER = 0
    RELEASE = 1


class Event:
    def __init__(self, kind: EventKind, time: float) -> None:
        self._kind = kind
        self._time = time

    @property
    def kind(self):
        return self._kind

    @property
    def time(self):
        return self._time
