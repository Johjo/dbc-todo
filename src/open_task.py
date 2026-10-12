from dataclasses import dataclass
from uuid import UUID

from expression import Result, Error, Ok


@dataclass(frozen=True)
class TaskTag:
    uuid: UUID


@dataclass(frozen=True)
class TaskDescription:
    value: str


@dataclass(frozen=True)
class TaskTitle:
    value: str


@dataclass(frozen=True)
class TaskOpened:
    tags: tuple[TaskTag, ...]
    tag: TaskTag
    title: TaskTitle
    description: TaskDescription


@dataclass(frozen=True)
class Task:
    tag: TaskTag
    title: TaskTitle
    description: TaskDescription

    def as_opened(self) -> TaskOpened:
        return TaskOpened((self.tag,), self.tag, self.title, self.description)


@dataclass(frozen=True)
class TaskAlreadyOpened:
    tag: TaskTag


@dataclass(frozen=True)
class History:
    events: tuple[TaskOpened, ...]

    @classmethod
    def build(cls, *events: TaskOpened) -> "History":
        return cls(events=tuple(events))

    @classmethod
    def empty(cls) -> "History":
        return cls(events=())


class OpenTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, task: Task) -> Result[TaskOpened, TaskAlreadyOpened]:
        for event in self._history.events:
            if task.tag in event.tags:
                return Error(TaskAlreadyOpened(task.tag))

        return Ok(task.as_opened())
