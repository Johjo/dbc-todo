import uuid
from dataclasses import dataclass

from expression import Ok, Result


@dataclass(frozen=True)
class TaskTag:
    uuid: uuid.UUID




@dataclass(frozen=True)
class TaskOpened:
    tags: tuple[TaskTag, ...]


class OpenTask:
    def execute(self, tag: TaskTag) -> Result[TaskOpened, None]:
        return Ok(TaskOpened(tags=(tag,)))




class TestOpenTask:
    def test_open_task(self):
        tag = TaskTag(uuid=uuid.uuid4())
        actual = OpenTask().execute(tag)

        assert actual == Ok(TaskOpened(tags=(tag,)))

    def test_cannot_open_task_already_opened(self):
        tag = TaskTag(uuid=uuid.uuid4())
        
        actual = OpenTask().execute(tag)

        # assert actual == Ok(TaskOpened(tags=(tag,)))