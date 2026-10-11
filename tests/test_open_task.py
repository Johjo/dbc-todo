from dataclasses import dataclass


class OpenTask:
    def execute(self):
        pass


@dataclass(frozen=True)
class TaskId:
    pass


class TestOpenTask:
    def test_open_task(self):
        TaskId()
        OpenTask().execute()