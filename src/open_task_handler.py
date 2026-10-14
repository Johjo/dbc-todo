from commands import OpenTaskCommand
from errors import TaskAlreadyOpened
from event_store import EventStore
from events import TaskOpened
from expression import Result
from open_task import OpenTask


class OpenTaskHandler:
    def __init__(self, store: EventStore) -> None:
        self._store = store

    def __call__(self, command: OpenTaskCommand) -> Result[TaskOpened, TaskAlreadyOpened]:
        result = OpenTask(self._store.history()).execute(command.task)
        self._persist(result)
        return result

    def _persist(self, result: Result[TaskOpened, TaskAlreadyOpened]) -> None:
        match result:
            case Result(tag="ok", ok=event):
                self._store.append(event)
            case _:
                pass
