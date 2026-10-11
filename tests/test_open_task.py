from dataclasses import dataclass


@dataclass(frozen=True)
class TaskKey:
    pass


class OpenTask:
    def execute(self, key: TaskKey):
        pass


@dataclass(frozen=True)
class TaskOpened:
    pass


class TestOpenTask:
    def test_open_task(self):

        key = TaskKey()
        actual = OpenTask().execute(key)

        TaskOpened()