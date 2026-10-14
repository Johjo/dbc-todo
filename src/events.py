from dataclasses import dataclass, replace
from typing import TYPE_CHECKING
from value_objects import TaskTag, TaskTitle, TaskDescription


if TYPE_CHECKING:
    from history import History

@dataclass(frozen=True)
class Event:
    def __add__(self, history: "History") -> "History":
        return replace(history, events=((self,) + history.events))


@dataclass(frozen=True)
class TaskOpened(Event):
    tags: tuple[TaskTag, ...]
    title: TaskTitle
    description: TaskDescription


@dataclass(frozen=True)
class TaskClosed(Event):
    tags: tuple[TaskTag, ...]


@dataclass(frozen=True)
class TaskReopened(Event):
    tags: tuple[TaskTag, ...]
