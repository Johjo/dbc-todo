from dataclasses import replace
from uuid import UUID

import hypothesis.strategies as st
from expression import Ok, Error
from hypothesis import given
from open_task import OpenTask
from history import History
from task import Task
from errors import TaskAlreadyOpened
from events import TaskOpened
from value_objects import TaskTag
from tests.fixtures import a_task, any_task


class TestOpenTask:
    @given(st.integers(min_value=0, max_value=50), any_task)
    def test_cannot_open_task_already_opened(self, history_size: int, task: Task):
        task = replace(task, tag=(TaskTag(uuid=UUID(int=history_size))))
        other_events = (a_task(uuid=UUID(int=i)).as_opened() for i in range(history_size))
        history = History.build(*other_events, task.as_opened())

        actual = OpenTask(history=history).execute(task)

        assert actual == Error(TaskAlreadyOpened(TaskTag(uuid=UUID(int=history_size))))


    @given(st.integers(min_value=0, max_value=50), any_task)
    def test_can_open_task_even_if_others_tasks_are_opened(self, history_size: int, task: Task):
        other_events = (a_task(uuid=i).as_opened() for i in range(history_size))
        history = History.build(*other_events)

        actual = OpenTask(history=history).execute(task)

        assert actual == Ok(TaskOpened(tags=(task.tag,), title=task.title, description=task.description))