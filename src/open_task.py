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
            match event:
                case TaskOpened(tags=tags):
                    if task.tag in tags:
                        return Error(TaskAlreadyOpened(task.tag))
                case _:
                    pass

        return Ok(task.as_opened())
