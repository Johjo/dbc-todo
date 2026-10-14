from dataclasses import dataclass

from command_bus import CommandBus
from errors import HandlerNotFound
from expression import Error, Ok


@dataclass(frozen=True)
class Command:
    value: str


def its_handler(command: Command) -> object:
    return Ok(command)


class TestCommandBus:
    def test_dispatches_command_to_its_handler(self):
        bus = CommandBus({Command: its_handler})
        command = Command(value=".")
        assert bus.dispatch(command) == Ok(command)

    def test_cannot_dispatch_command_without_handler(self):
        bus = CommandBus({})
        command = Command(value=".")
        assert bus.dispatch(command) == Error(HandlerNotFound(command=command))
