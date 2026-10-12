from dataclasses import dataclass

from close_task import CloseTask
from errors import TaskNotFound
from events import TaskClosed
from expression import Error, Ok
from history import History
from tests.fixtures import a_task
from value_objects import TaskTag


@dataclass(frozen=True)
class TaskAlreadyClosed:
    tag: TaskTag


class TestCloseTask:
    def test_cannot_close_task_which_is_not_open(self):
        assert CloseTask(History.empty()).execute(a_task().tag) == Error(TaskNotFound())

    def test_can_close_open_task(self):
        task = a_task()
        history = History.build(task.as_opened())
        assert CloseTask(history).execute(task.tag) == Ok(TaskClosed(tags=(task.tag,)))

    def test_cannot_close_task_already_closed(self):
        task = a_task()
        history = History.build(task.as_opened())
        TaskAlreadyClosed(tag=task.tag)
        # assert CloseTask(history).execute() == Ok(TaskClosed())

