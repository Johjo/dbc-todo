from errors import TaskAlreadyOpened
from events import TaskOpened
from expression import Result, Error, Ok
from history import History
from task import Task


class OpenTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, task: Task) -> Result[TaskOpened, TaskAlreadyOpened]:
        for event in self._history.events:
            if task.tag in event.tags:
                return Error(TaskAlreadyOpened(task.tag))

        return Ok(task.as_opened())
