from dataclasses import dataclass

from expression import Error, Result, Ok
from open_task import History, TaskOpened
from tests.fixtures import a_task


@dataclass(frozen=True)
class TaskNotFound:
    pass


class CloseTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self) -> Result[None, TaskNotFound]:
        return Error(TaskNotFound())

@dataclass(frozen=True)
class TaskClosed:
    pass


class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        assert CloseTask(History.empty()).execute() == Error(TaskNotFound())

    def test_can_close_open_task(self):
        task = a_task()
        history = History.build(task.as_opened())
        # assert CloseTask().execute() == Ok(TaskClosed())
