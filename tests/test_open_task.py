from dataclasses import dataclass


@dataclass(frozen=True)
class TaskKey:
    pass


@dataclass(frozen=True)
class TaskOpened:
    pass


class OpenTask:
    def execute(self, key: TaskKey) -> TaskOpened:
        return TaskOpened()




class TestOpenTask:
    def test_open_task(self):

        key = TaskKey()
        actual = OpenTask().execute(key)

        assert actual == TaskOpened()