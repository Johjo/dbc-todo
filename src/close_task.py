from errors import TaskNotFound, TaskAlreadyClosed
from events import TaskClosed, TaskOpened
from expression import Result, Ok, Error
from history import History
from value_objects import TaskTag


class CloseTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, tag: TaskTag) -> Result[TaskClosed, TaskNotFound | TaskAlreadyClosed]:
        opened = False
        for event in self._history.events:
            match event:
                case TaskClosed(tags=tags) if tag in tags:
                    return Error(TaskAlreadyClosed(tag=tag))
                case TaskOpened(tags=tags) if tag in tags:
                    opened = True

        if not opened:
            return Error(TaskNotFound())
        return Ok(TaskClosed(tags=(tag,)))
