from dataclasses import dataclass

from expression import Error, Result, Ok
from open_task import History, TaskOpened
from tests.fixtures import a_task


@dataclass(frozen=True)
class TaskNotFound:
    pass


@dataclass(frozen=True)
class TaskClosed:
    pass


class CloseTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self) -> Result[TaskClosed, TaskNotFound]:
        if len(self._history.events ) == 1:
            return Ok(TaskClosed())
        return Error(TaskNotFound())



class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        assert CloseTask(History.empty()).execute() == Error(TaskNotFound())

    def test_can_close_open_task(self):
        task = a_task()
        history = History.build(task.as_opened())
        assert CloseTask(history).execute() == Ok(TaskClosed())

    def test_cannot_close_task_already_closed(self):
        task = a_task()
        history = History.build(task.as_opened())
        # assert CloseTask(history).execute() == Ok(TaskClosed())

