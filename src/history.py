from dataclasses import dataclass

from events import TaskOpened


@dataclass(frozen=True)
class History:
    events: tuple[TaskOpened, ...]

    @classmethod
    def build(cls, *events: TaskOpened) -> "History":
        return cls(events=tuple(events))

    @classmethod
    def empty(cls) -> "History":
        return cls(events=())
