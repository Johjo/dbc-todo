from collections.abc import Callable, Mapping
from typing import Any

from errors import HandlerNotFound
from expression import Error

Handler = Callable[[Any], Any]


class CommandBus:
    def __init__(self, handlers: Mapping[type[object], Handler]) -> None:
        self._handlers = handlers

    def dispatch(self, command: object) -> object:
        handler = self._handlers.get(type(command))
        if handler is None:
            return Error(HandlerNotFound(command=command))
        result: object = handler(command)
        return result
