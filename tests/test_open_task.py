import uuid
from dataclasses import dataclass

from expression import Ok, Result


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
class History:
    events: tuple[TaskOpened, ...]
    @classmethod
    def build(cls, *events: TaskOpened) -> "History":
        return cls(events=tuple(events))

class OpenTask:
    def __init__(self, history: tuple[TaskOpened, ...]):
        self._history = history

    def execute(self, tag: TaskTag) -> Result[TaskOpened, None]:
        return Ok(TaskOpened(tags=(tag,)))




class TestOpenTask:
    def test_open_task(self):
        tag = TaskTag(uuid=uuid.uuid4())
        actual = OpenTask(history=()).execute(tag)

        assert actual == Ok(TaskOpened(tags=(tag,)))

    def test_cannot_open_task_already_opened(self):
        tag = TaskTag(uuid=uuid.uuid4())
        history = (TaskOpened.build(tag), )
        actual = OpenTask(history=history).execute(tag)

        # assert actual == Ok(TaskOpened(tags=(tag,)))