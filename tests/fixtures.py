from collections.abc import Callable, Sequence
from uuid import UUID

from expression import Result
from hypothesis import strategies as st
from task import Task
from value_objects import TaskTag, TaskDescription, TaskTitle

from close_task import CloseTask
from errors import TaskAlreadyOpened, TaskAlreadyClosed, TaskNotFound, TaskNotClosed
from events import TaskClosed, TaskOpened, TaskReopened
from history import History
from open_task import OpenTask
from reopen_task import ReopenTask

UuidOrInt = UUID | int


def a_task(title: str = ".", description: str = ".", uuid: UuidOrInt = 999) -> Task:
    return Task(tag=(TaskTag(uuid=to_uuid(uuid))), title=TaskTitle(title), description=TaskDescription(description))


def to_uuid(uuid: UUID | int) -> UUID:
    match uuid:
        case UUID():
            return uuid
        case int():
            return UUID(int=uuid)
        case _: # pragma: no cover
            pass


task_tags = st.builds(TaskTag, uuid=st.uuids())
task_titles = st.text(min_size=1, max_size=50).map(lambda s: TaskTitle(s))
task_descriptions = st.text(max_size=500).map(lambda s: TaskDescription(s))
any_task = st.builds(
    Task,
    tag=task_tags,
    title=task_titles,
    description=task_descriptions,
)

MAX_TASKS = 10
MAX_ACTIONS = 10

CommandResult = (
    Result[TaskOpened, TaskAlreadyOpened]
    | Result[TaskClosed, TaskNotFound | TaskAlreadyClosed]
    | Result[TaskReopened, TaskNotFound | TaskNotClosed]
)
Action = tuple[Callable[[History, int], CommandResult], int]


def open_task(history: History, uuid: int) -> CommandResult:
    return OpenTask(history).execute(a_task(uuid=uuid))


def close_task(history: History, uuid: int) -> CommandResult:
    return CloseTask(history).execute(TaskTag(uuid=to_uuid(uuid)))


def reopen_task(history: History, uuid: int) -> CommandResult:
    return ReopenTask(history).execute(TaskTag(uuid=to_uuid(uuid)))


def play(actions: Sequence[Action]) -> History:
    history = History.empty()
    for command, uuid in actions:
        result = command(history, uuid)
        match result:
            case Result(tag="ok", ok=event):
                history = History.build(*history.events, event)
            case _:
                pass
    return history


def any_history(
    max_tasks: int = MAX_TASKS,
    max_actions: int = MAX_ACTIONS,
) -> st.SearchStrategy[History]:
    return st.lists(
        st.tuples(st.sampled_from((open_task, close_task, reopen_task)), st.integers(min_value=0, max_value=max_tasks - 1)),
        min_size=1,
        max_size=max_actions,
    ).map(play)
