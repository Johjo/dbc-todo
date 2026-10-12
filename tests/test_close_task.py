from close_task import CloseTask
from errors import TaskNotFound, TaskAlreadyClosed
from events import TaskClosed
from expression import Error, Ok
from history import History
from hypothesis import given
from tests.fixtures import a_task, any_history


class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        assert CloseTask(History.empty()).execute(a_task().tag) == Error(TaskNotFound())

    @given(any_history())
    def test_can_close_open_task(self, history: History):
        task = a_task()
        history = task.as_opened() + history
        assert CloseTask(history).execute(task.tag) == Ok(TaskClosed(tags=(task.tag,)))

    @given(any_history())
    def test_cannot_close_task_already_closed(self, history: History):
        task = a_task()
        history = task.as_opened() + History.build(*history.events) + task.as_closed()
        assert CloseTask(history).execute(task.tag) == Error(TaskAlreadyClosed(tag=task.tag))

