from dataclasses import dataclass

from expression import Error

class CloseTask:
    def execute(self) -> None:
        pass

@dataclass(frozen=True)
class TaskNotFound:
    pass


class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        Error(TaskNotFound())
        # assert CloseTask().execute() == Error()