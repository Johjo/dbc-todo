from errors import TaskNotFound, TaskAlreadyClosed
from events import TaskClosed, TaskOpened, TaskReopened
from expression import Result, Ok, Error
from history import History
from value_objects import TaskTag


class CloseTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, tag: TaskTag) -> Result[TaskClosed, TaskNotFound | TaskAlreadyClosed]:
        found = False
        opened = False
        for event in self._history.events:
            match event:
                case TaskOpened(tags=tags) if tag in tags:
                    found = True
                    opened = True
                case TaskReopened(tags=tags) if tag in tags:
                    found = True
                    opened = True
                case TaskClosed(tags=tags) if tag in tags:
                    found = True
                    opened = False

        if not found:
            return Error(TaskNotFound())
        if not opened:
            return Error(TaskAlreadyClosed(tag=tag))
        return Ok(TaskClosed(tags=(tag,)))
