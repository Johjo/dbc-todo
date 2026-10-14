from event_store import InMemoryEventStore
from history import History
from hypothesis import given
from tests.fixtures import any_history


class TestInMemoryEventStore:
    def test_starts_empty(self):
        assert InMemoryEventStore().history() == History.empty()

    @given(any_history())
    def test_returns_appended_events_in_order(self, history: History):
        store = InMemoryEventStore()
        for event in history.events:
            store.append(event)
        assert store.history() == history
