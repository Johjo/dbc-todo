from dataclasses import dataclass


@dataclass(frozen=True)
class TaskKey:
    pass


class OpenTask:
    def execute(self, key: TaskKey):
        pass


class TestOpenTask:
    def test_open_task(self):

        OpenTask().execute(TaskKey())