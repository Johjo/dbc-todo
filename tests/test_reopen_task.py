from errors import TaskNotFound, TaskNotClosed
from events import TaskReopened
from expression import Error, Ok
from history import History
from hypothesis import given
from reopen_task import ReopenTask
from tests.fixtures import a_task, any_history


class TestReopenTask:
    @given(any_history())
    def test_cannot_reopen_task_which_is_not_closed(self, history: History):
        assert ReopenTask(history).execute(a_task().tag) == Error(TaskNotFound())

    @given(any_history())
    def test_can_reopen_closed_task(self, history: History):
        task = a_task()
        history = task.as_opened() + History.build(*history.events) + task.as_closed()
        assert ReopenTask(history).execute(task.tag) == Ok(TaskReopened(tags=(task.tag,)))

    @given(any_history())
    def test_cannot_reopen_task_which_is_open(self, history: History):
        task = a_task()
        history = task.as_opened() + history
        assert ReopenTask(history).execute(task.tag) == Error(TaskNotClosed(tag=task.tag))
