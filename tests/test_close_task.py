from dataclasses import dataclass

from expression import Error, Result
from open_task import History, TaskOpened
from tests.fixtures import a_task


@dataclass(frozen=True)
class TaskNotFound:
    pass


class CloseTask:
    def execute(self) -> Result[None, TaskNotFound]:
        return Error(TaskNotFound())

class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        assert CloseTask().execute() == Error(TaskNotFound())

    def test_can_close_open_task(self):
        history = History.build(a_task().as_opened())
