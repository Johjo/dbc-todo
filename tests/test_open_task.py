from uuid import UUID, uuid4
from dataclasses import dataclass

import hypothesis.strategies as st
from expression import Ok, Result, Error
from hypothesis import given
from typing import NewType

@dataclass(frozen=True)
class TaskTag:
    uuid: UUID

TaskTitle = NewType("TaskTitle", str)
TaskDescription = NewType("TaskDescription", str)

@dataclass(frozen=True)
class Task:
    tag: TaskTag
    title: TaskTitle
    description: TaskDescription



@dataclass(frozen=True)
class TaskOpened:
    tags: tuple[TaskTag, ...]

    @classmethod
    def build(cls, *tags: TaskTag) -> "TaskOpened":
        return cls(tags=tuple(tags))

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

    def execute(self, task_or_tag: TaskTag | Task) -> Result[TaskOpened, TaskAlreadyOpened]:
        match task_or_tag:
            case TaskTag() as tag:
                tag = tag
            case Task(tag=tag):
                tag = tag

        for event in self._history.events:
            if tag in event.tags:
                return Error(TaskAlreadyOpened(tag))

        return Ok(TaskOpened(tags=(tag,)))


def a_task(title: str, description: str, uuid: UUID) -> Task:
    return Task(tag=(TaskTag(uuid=uuid)), title=TaskTitle(title), description=TaskDescription(description))


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
    @given(any_task)
    def test_open_task(self, task: Task):
        actual = OpenTask(history=History.empty()).execute(task)

        assert actual == Ok(TaskOpened.build(task.tag))

    @given(st.integers(min_value=0, max_value=50))
    def test_cannot_open_task_already_opened(self, history_size: int):
        tag = TaskTag(uuid=UUID(int=history_size))
        other_events = (TaskOpened.build(TaskTag(uuid=UUID(int=i))) for i in range(history_size))
        the_event = TaskOpened.build(tag)
        history = History.build(*other_events, the_event)

        actual = OpenTask(history=history).execute(tag)

        assert actual == Error(TaskAlreadyOpened(tag))


    @given(st.integers(min_value=0, max_value=50))
    def test_can_open_task_even_if_others_tasks_are_opened(self, history_size: int):
        new_task = TaskTag(uuid=UUID(int=history_size))
        other_events = (TaskOpened.build(TaskTag(uuid=UUID(int=i))) for i in range(history_size))
        history = History.build(*other_events)

        actual = OpenTask(history=history).execute(new_task)

        assert actual == Ok(TaskOpened.build(new_task))