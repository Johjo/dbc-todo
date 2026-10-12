from dataclasses import dataclass

from value_objects import TaskTag, TaskTitle, TaskDescription


@dataclass(frozen=True)
class TaskOpened:
    tags: tuple[TaskTag, ...]
    title: TaskTitle
    description: TaskDescription
