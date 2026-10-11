import uuid
from dataclasses import dataclass

import hypothesis.strategies as st
from expression import Ok, Result, Error
from hypothesis import given
from typing_extensions import NewType


@dataclass(frozen=True)
class TaskTag:
    uuid: uuid.UUID

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

    def execute(self, task_or_tag: TaskTag) -> Result[TaskOpened, TaskAlreadyOpened]:
        match task_or_tag:
            case TaskTag() as tag:
                tag = tag
            # case Task(tag=tag):
            #     tag = tag

        for event in self._history.events:
            if tag in event.tags:
                return Error(TaskAlreadyOpened(task_or_tag))

        return Ok(TaskOpened(tags=(task_or_tag,)))




class TestOpenTask:
    def test_open_task(self):
        tag = TaskTag(uuid=uuid.uuid4())
        actual = OpenTask(history=History.empty()).execute(tag)

        assert actual == Ok(TaskOpened(tags=(tag,)))

    @given(st.integers(min_value=0, max_value=50))
    def test_cannot_open_task_already_opened(self, history_size: int):
        tag = TaskTag(uuid=uuid.UUID(int=history_size))
        other_events = (TaskOpened.build(TaskTag(uuid=uuid.UUID(int=i))) for i in range(history_size))
        the_event = TaskOpened.build(tag)
        history = History.build(*other_events, the_event)

        actual = OpenTask(history=history).execute(tag)

        assert actual == Error(TaskAlreadyOpened(tag))


    @given(st.integers(min_value=0, max_value=50))
    def test_can_open_task_even_if_others_tasks_are_opened(self, history_size: int):
        new_task = TaskTag(uuid=uuid.UUID(int=history_size))
        other_events = (TaskOpened.build(TaskTag(uuid=uuid.UUID(int=i))) for i in range(history_size))
        history = History.build(*other_events)

        actual = OpenTask(history=history).execute(new_task)

        assert actual == Ok(TaskOpened.build(new_task))