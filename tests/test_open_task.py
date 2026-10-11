from dataclasses import dataclass


@dataclass(frozen=True)
class TaskId:
    pass


class OpenTask:
    def execute(self, key: TaskId):
        pass




class TestOpenTask:
    def test_open_task(self):

        OpenTask().execute(TaskId())