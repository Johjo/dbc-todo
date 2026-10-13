from errors import TaskNotFound, TaskNotClosed
from events import TaskClosed, TaskOpened, TaskReopened
from expression import Result, Ok, Error
from history import History
from value_objects import TaskTag


class ReopenTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, tag: TaskTag) -> Result[TaskReopened, TaskNotFound | TaskNotClosed]:
        found = False
        closed = False
        for event in self._history.events:
            match event:
                case TaskOpened(tags=tags) if tag in tags:
                    found = True
                    closed = False
                case TaskReopened(tags=tags) if tag in tags:
                    found = True
                    closed = False
                case TaskClosed(tags=tags) if tag in tags:
                    found = True
                    closed = True

        if not found:
            return Error(TaskNotFound())
        if not closed:
            return Error(TaskNotClosed(tag=tag))
        return Ok(TaskReopened(tags=(tag,)))
