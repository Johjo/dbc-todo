from close_task import CloseTask
from errors import TaskNotFound
from events import TaskClosed
from expression import Error, Ok
from history import History
from tests.fixtures import a_task


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

