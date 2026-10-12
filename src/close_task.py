from errors import TaskNotFound
from events import TaskClosed
from expression import Result, Ok, Error
from history import History
from value_objects import TaskTag


class CloseTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, tag: TaskTag) -> Result[TaskClosed, TaskNotFound]:
        if len(self._history.events ) == 1:
            return Ok(TaskClosed())
        return Error(TaskNotFound())
