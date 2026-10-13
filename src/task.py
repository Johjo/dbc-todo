from dataclasses import dataclass

from events import TaskOpened, TaskClosed, TaskReopened
from value_objects import TaskTag, TaskTitle, TaskDescription


@dataclass(frozen=True)
class Task:
    tag: TaskTag
    title: TaskTitle
    description: TaskDescription

    def as_opened(self) -> TaskOpened:
        return TaskOpened(tags=(self.tag,), title=self.title, description=self.description)

    def as_closed(self) -> TaskClosed:
        return TaskClosed(tags=(self.tag,))

    def as_reopened(self) -> TaskReopened:
        return TaskReopened(tags=(self.tag,))
