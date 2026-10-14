from commands import ReopenTaskCommand
from errors import TaskNotClosed, TaskNotFound
from event_store import EventStore
from events import TaskReopened
from expression import Result
from reopen_task import ReopenTask


class ReopenTaskHandler:
    def __init__(self, store: EventStore) -> None:
        self._store = store

    def __call__(self, command: ReopenTaskCommand) -> Result[TaskReopened, TaskNotFound | TaskNotClosed]:
        result = ReopenTask(self._store.history()).execute(command.tag)
        self._persist(result)
        return result

    def _persist(self, result: Result[TaskReopened, TaskNotFound | TaskNotClosed]) -> None:
        match result:
            case Result(tag="ok", ok=event):
                self._store.append(event)
            case _:
                pass
