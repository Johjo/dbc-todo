from command_bus import CommandBus
from commands import OpenTaskCommand
from errors import TaskAlreadyOpened
from event_store import InMemoryEventStore
from expression import Error, Ok
from history import History
from hypothesis import given
from open_task_handler import OpenTaskHandler
from tests.fixtures import a_task, any_history


class TestOpenTaskHandler:
    @given(any_history())
    def test_can_open_task(self, history: History):
        store = InMemoryEventStore()
        for event in history.events:
            store.append(event)
        bus = CommandBus({OpenTaskCommand: OpenTaskHandler(store)})
        task = a_task()
        assert bus.dispatch(OpenTaskCommand(task=task)) == Ok(task.as_opened())
        assert store.history() == History.build(*history.events, task.as_opened())

    @given(any_history())
    def test_cannot_open_task_already_opened(self, history: History):
        store = InMemoryEventStore()
        task = a_task()
        for event in (task.as_opened(), *history.events):
            store.append(event)
        bus = CommandBus({OpenTaskCommand: OpenTaskHandler(store)})
        assert bus.dispatch(OpenTaskCommand(task=task)) == Error(TaskAlreadyOpened(task.tag))
        assert store.history() == History.build(task.as_opened(), *history.events)
