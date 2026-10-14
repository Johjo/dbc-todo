from dataclasses import dataclass

from task import Task
from value_objects import TaskTag


@dataclass(frozen=True)
class OpenTaskCommand:
    task: Task


@dataclass(frozen=True)
class CloseTaskCommand:
    tag: TaskTag
