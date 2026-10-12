from dataclasses import dataclass

from value_objects import TaskTag


@dataclass(frozen=True)
class TaskAlreadyOpened:
    tag: TaskTag


@dataclass(frozen=True)
class TaskNotFound:
    pass
