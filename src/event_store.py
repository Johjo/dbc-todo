from abc import ABC, abstractmethod

from events import Event
from history import History


class EventStore(ABC):
    @abstractmethod
    def history(self) -> History: ...

    @abstractmethod
    def append(self, event: Event) -> None: ...


class InMemoryEventStore(EventStore):
    def __init__(self) -> None:
        self._history = History.empty()

    def history(self) -> History:
        return self._history

    def append(self, event: Event) -> None:
        self._history = self._history + event
