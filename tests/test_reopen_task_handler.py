from command_bus import CommandBus
from commands import ReopenTaskCommand
from errors import TaskNotClosed
from event_store import InMemoryEventStore
from events import TaskReopened
from expression import Error, Ok
from history import History
from hypothesis import given
from reopen_task_handler import ReopenTaskHandler
from tests.fixtures import a_task, any_history


class TestReopenTaskHandler:
    @given(any_history())
    def test_can_reopen_task(self, history: History):
        store = InMemoryEventStore()
        task = a_task()
        for event in (task.as_opened(), task.as_closed(), *history.events):
            store.append(event)
        bus = CommandBus({ReopenTaskCommand: ReopenTaskHandler(store)})
        reopened = TaskReopened(tags=(task.tag,))
        assert bus.dispatch(ReopenTaskCommand(tag=task.tag)) == Ok(reopened)
        assert store.history() == History.build(task.as_opened(), task.as_closed(), *history.events, reopened)

    @given(any_history())
    def test_cannot_reopen_task_which_is_open(self, history: History):
        store = InMemoryEventStore()
        task = a_task()
        for event in (task.as_opened(), *history.events):
            store.append(event)
        bus = CommandBus({ReopenTaskCommand: ReopenTaskHandler(store)})
        assert bus.dispatch(ReopenTaskCommand(tag=task.tag)) == Error(TaskNotClosed(tag=task.tag))
        assert store.history() == History.build(task.as_opened(), *history.events)
