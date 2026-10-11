from dataclasses import replace
from uuid import UUID

import hypothesis.strategies as st
from expression import Ok, Error
from hypothesis import given
from open_task import TaskTag, TaskDescription, TaskTitle, TaskOpened, Task, TaskAlreadyOpened, History, OpenTask

UuidOrInt = UUID | int

def a_task(title: str = ".", description: str = ".", uuid: UuidOrInt = 999) -> Task:
    return Task(tag=(TaskTag(uuid=to_uuid(uuid))), title=TaskTitle(title), description=TaskDescription(description))


def to_uuid(uuid: UUID | int) -> UUID:
    match uuid:
        case UUID():
            return uuid
        case int():
            return UUID(int=uuid)


task_tags = st.builds(TaskTag, uuid=st.uuids())

task_titles = st.text(min_size=1, max_size=50).map(lambda s: TaskTitle(s))

task_descriptions = st.text(max_size=500).map(lambda s: TaskDescription(s))

any_task = st.builds(
    Task,
    tag=task_tags,
    title=task_titles,
    description=task_descriptions,
)


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

        assert actual == Ok(TaskOpened(tags=(task.tag,), tag=task.tag, title=task.title, description=task.description))