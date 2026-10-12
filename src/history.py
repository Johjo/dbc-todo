from dataclasses import dataclass, replace

from events import TaskOpened, Event


@dataclass(frozen=True)
class History:
    events: tuple[Event, ...]

    def __add__(self, other: Event) -> "History":
        return replace(self, events=self.events + (other,))

    @classmethod
    def build(cls, *events: Event) -> "History":
        return cls(events=tuple(events))

    @classmethod
    def empty(cls) -> "History":
        return cls(events=())
