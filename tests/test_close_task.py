from dataclasses import dataclass

from expression import Error, Result


@dataclass(frozen=True)
class TaskNotFound:
    pass


class CloseTask:
    def execute(self) -> Result[None, TaskNotFound]:
        return Error(TaskNotFound())



class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        assert CloseTask().execute() == Error(TaskNotFound())
        # assert CloseTask().execute() == Error()