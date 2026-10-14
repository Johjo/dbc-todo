from close_task import CloseTask
from errors import TaskAlreadyClosed, TaskNotClosed
from events import TaskClosed, TaskReopened
from expression import Error, Ok
from history import History
from hypothesis import given
from hypothesis import strategies as st
from reopen_task import ReopenTask
from tests.fixtures import a_task, any_history


class TestTaskLifecycle:
    @given(any_history(), st.integers(min_value=0, max_value=10))
    def test_can_close_and_reopen_task_repeatedly(self, history: History, cycles: int):
        task = a_task()
        history = task.as_opened() + History.build(*history.events)
        for _ in range(cycles):
            history = history + task.as_closed()
            assert CloseTask(history).execute(task.tag) == Error(TaskAlreadyClosed(tag=task.tag))
            assert ReopenTask(history).execute(task.tag) == Ok(TaskReopened(tags=(task.tag,)))
            history = history + TaskReopened(tags=(task.tag,))
            assert ReopenTask(history).execute(task.tag) == Error(TaskNotClosed(tag=task.tag))
        assert CloseTask(history).execute(task.tag) == Ok(TaskClosed(tags=(task.tag,)))
