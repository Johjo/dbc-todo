from dataclasses import dataclass

from value_objects import TaskTag, TaskTitle, TaskDescription

@dataclass(frozen=True)
class Event:
    pass


@dataclass(frozen=True)
class TaskOpened(Event):
    tags: tuple[TaskTag, ...]
    title: TaskTitle
    description: TaskDescription


@dataclass(frozen=True)
class TaskClosed(Event):
    tags: tuple[TaskTag, ...] | None = None
