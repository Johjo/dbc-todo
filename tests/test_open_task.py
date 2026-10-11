import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class TaskTag:
    uuid: uuid.UUID




@dataclass(frozen=True)
class TaskOpened:
    tags: tuple[TaskTag, ...]


class OpenTask:
    def execute(self, tag: TaskTag) -> TaskOpened:
        return TaskOpened(tags=(tag,))




class TestOpenTask:
    def test_open_task(self):
        tag = TaskTag(uuid=uuid.uuid4())
        actual = OpenTask().execute(tag)

        assert actual == TaskOpened(tags=(tag,))