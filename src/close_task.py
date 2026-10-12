from dataclasses import dataclass

from events import Event
from expression import Result, Ok, Error
from history import History


@dataclass(frozen=True)
class TaskNotFound:
    pass


@dataclass(frozen=True)
class TaskClosed(Event):
    pass


class CloseTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self) -> Result[TaskClosed, TaskNotFound]:
        if len(self._history.events ) == 1:
            return Ok(TaskClosed())
        return Error(TaskNotFound())
