import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class TaskKey:
    uuid: uuid.UUID


@dataclass(frozen=True)
class TaskOpened:
    tag: tuple[TaskKey, ...]


class OpenTask:
    def execute(self, key: TaskKey) -> TaskOpened:
        return TaskOpened(())




class TestOpenTask:
    def test_open_task(self):
        key = TaskKey(uuid=uuid.uuid4())
        actual = OpenTask().execute(key)

        assert actual == TaskOpened(tag=())