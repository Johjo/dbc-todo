from uuid import UUID, uuid4
from dataclasses import dataclass, replace

import hypothesis.strategies as st
from expression import Ok, Result, Error
from hypothesis import given
from typing import NewType

@dataclass(frozen=True)
class TaskTag:
    uuid: UUID

@dataclass(frozen=True)
class TaskDescription:
    value: str

@dataclass(frozen=True)
class TaskTitle:
    value: str




@dataclass(frozen=True)
class TaskOpened:
    tags: tuple[TaskTag, ...]
    tag: TaskTag
    title: TaskTitle  | None = None
    description: TaskDescription | None = None

    @classmethod
    def build(cls, tag: TaskTag) -> "TaskOpened":
        return cls(tags=(tag,), tag=tag)

@dataclass(frozen=True)
class Task:
    tag: TaskTag
    title: TaskTitle
    description: TaskDescription

    def as_opened(self) -> TaskOpened:
        return TaskOpened((self.tag,), self.tag, self.title)

@dataclass(frozen=True)
class TaskAlreadyOpened:
    tag: TaskTag

@dataclass(frozen=True)
class History:
    events: tuple[TaskOpened, ...]

    @classmethod
    def build(cls, *events: TaskOpened) -> "History":
        return cls(events=tuple(events))

    @classmethod
    def empty(cls) -> "History":
        return cls(events=())

class OpenTask:
    def __init__(self, history: History):
        self._history = history

    def execute(self, task: Task) -> Result[TaskOpened, TaskAlreadyOpened]:
        for event in self._history.events:
            if task.tag in event.tags:
                return Error(TaskAlreadyOpened(task.tag))

        return Ok(task.as_opened())


UuidOrInt = UUID | int

def a_task(title: str = ".", description: str = ".", uuid: UuidOrInt = 999) -> Task:
    return Task(tag=(TaskTag(uuid=to_uuid(uuid))), title=TaskTitle(title), description=TaskDescription(description))


def to_uuid(uuid: UUID | int) -> UUID:
    match uuid:
        case UUID():
            u = uuid
        case int():
            u = UUID(int=uuid)
    return u


task_tags = st.builds(TaskTag, uuid=st.uuids())

task_titles = st.text(min_size=1, max_size=50).map(TaskTitle)

task_descriptions = st.text(max_size=500).map(TaskDescription)

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
        other_events = (TaskOpened.build(TaskTag(uuid=UUID(int=i))) for i in range(history_size))
        history = History.build(*other_events)

        actual = OpenTask(history=history).execute(task)

        assert actual == Ok(TaskOpened(tags=(task.tag, ), tag=task.tag, title=task.title))