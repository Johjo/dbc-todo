from dataclasses import dataclass

from events import TaskOpened, Event


@dataclass(frozen=True)
class History:
    events: tuple[Event, ...]

    @classmethod
    def build(cls, *events: Event) -> "History":
        return cls(events=tuple(events))

    @classmethod
    def empty(cls) -> "History":
        return cls(events=())
