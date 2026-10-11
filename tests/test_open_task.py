import uuid
from dataclasses import dataclass

from expression import Ok, Result, Error


@dataclass(frozen=True)
class TaskTag:
    uuid: uuid.UUID




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

    def execute(self, tag: TaskTag) -> Result[TaskOpened, TaskAlreadyOpened]:
        if len(self._history.events) > 0:
            if tag in self._history.events[0].tags:
                return Error(TaskAlreadyOpened(tag))
        return Ok(TaskOpened(tags=(tag,)))




class TestOpenTask:
    def test_open_task(self):
        tag = TaskTag(uuid=uuid.uuid4())
        actual = OpenTask(history=History.empty()).execute(tag)

        assert actual == Ok(TaskOpened(tags=(tag,)))

    def test_cannot_open_task_already_opened(self):
        tag = TaskTag(uuid=uuid.uuid4())
        history = History.build(TaskOpened.build(tag))

        actual = OpenTask(history=history).execute(tag)

        assert actual == Error(TaskAlreadyOpened(tag))


    def test_can_open_task_even_if_others_tasks_are_opened(self):
        existing_tag = TaskTag(uuid=uuid.UUID(int=1))
        new_task = TaskTag(uuid=uuid.UUID(int=2))
        history = History.build(TaskOpened.build(existing_tag))

        actual = OpenTask(history=history).execute(new_task)

        assert actual == Ok(TaskOpened.build(new_task))