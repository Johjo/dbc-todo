from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TaskTag:
    uuid: UUID


@dataclass(frozen=True)
class TaskDescription:
    value: str


@dataclass(frozen=True)
class TaskTitle:
    value: str
