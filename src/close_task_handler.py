from close_task import CloseTask
from commands import CloseTaskCommand
from errors import TaskAlreadyClosed, TaskNotFound
from event_store import EventStore
from events import TaskClosed
from expression import Result
from value_objects import TaskTag


class CloseTaskHandler:
    def __init__(self, store: EventStore) -> None:
        self._store = store

    def __call__(self, command: CloseTaskCommand) -> Result[TaskClosed, TaskNotFound | TaskAlreadyClosed]:
        result = CloseTask(self._store.history()).execute(command.tag)
        self._persist(result)
        return result

    def _persist(self, result: Result[TaskClosed, TaskNotFound | TaskAlreadyClosed]) -> None:
        match result:
            case Result(tag="ok", ok=event):
                self._store.append(event)
            case _:
                pass
