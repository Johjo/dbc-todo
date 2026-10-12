from uuid import UUID

from hypothesis import strategies as st
from task import Task
from value_objects import TaskTag, TaskDescription, TaskTitle

UuidOrInt = UUID | int


def a_task(title: str = ".", description: str = ".", uuid: UuidOrInt = 999) -> Task:
    return Task(tag=(TaskTag(uuid=to_uuid(uuid))), title=TaskTitle(title), description=TaskDescription(description))


def to_uuid(uuid: UUID | int) -> UUID:
    match uuid:
        case UUID():
            return uuid
        case int():
            return UUID(int=uuid)


task_tags = st.builds(TaskTag, uuid=st.uuids())
task_titles = st.text(min_size=1, max_size=50).map(lambda s: TaskTitle(s))
task_descriptions = st.text(max_size=500).map(lambda s: TaskDescription(s))
any_task = st.builds(
    Task,
    tag=task_tags,
    title=task_titles,
    description=task_descriptions,
)
