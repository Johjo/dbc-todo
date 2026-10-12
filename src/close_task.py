from errors import TaskNotFound, TaskAlreadyClosed
from events import TaskClosed
from expression import Result, Ok, Error
from history import History
from value_objects import TaskTag


class CloseTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, tag: TaskTag) -> Result[TaskClosed, TaskNotFound | TaskAlreadyClosed]:
        if len(self._history.events ) == 1:
            return Ok(TaskClosed(tags=(tag,)))
        return Error(TaskNotFound())
