from command_bus import CommandBus
from commands import CloseTaskCommand
from errors import TaskAlreadyClosed
from event_store import InMemoryEventStore
from events import TaskClosed
from expression import Error, Ok
from history import History
from hypothesis import given
from close_task_handler import CloseTaskHandler
from tests.fixtures import a_task, any_history


class TestCloseTaskHandler:
    @given(any_history())
    def test_can_close_task(self, history: History):
        store = InMemoryEventStore()
        task = a_task()
        for event in (task.as_opened(), *history.events):
            store.append(event)
        bus = CommandBus({CloseTaskCommand: CloseTaskHandler(store)})
        closed = TaskClosed(tags=(task.tag,))
        assert bus.dispatch(CloseTaskCommand(tag=task.tag)) == Ok(closed)
        assert store.history() == History.build(task.as_opened(), *history.events, closed)

    @given(any_history())
    def test_cannot_close_task_already_closed(self, history: History):
        store = InMemoryEventStore()
        task = a_task()
        for event in (task.as_opened(), task.as_closed(), *history.events):
            store.append(event)
        bus = CommandBus({CloseTaskCommand: CloseTaskHandler(store)})
        assert bus.dispatch(CloseTaskCommand(tag=task.tag)) == Error(TaskAlreadyClosed(tag=task.tag))
        assert store.history() == History.build(task.as_opened(), task.as_closed(), *history.events)
