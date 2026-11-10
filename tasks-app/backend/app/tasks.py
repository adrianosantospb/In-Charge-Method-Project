"""Task routes. Every query filters by the signed-in user."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.auth import CurrentUser, SessionDep
from app.models import Task, TaskCreate, TaskRead, TaskUpdate, utc_now

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _own_task(session: SessionDep, user: CurrentUser, task_id: UUID) -> Task:
    task = session.exec(select(Task).where(Task.id == task_id, Task.owner_id == user.id)).first()
    if task is None:
        # 404, not 403: another user's task must look the same as one that does not exist.
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task


@router.get("", response_model=list[TaskRead])
def list_tasks(session: SessionDep, user: CurrentUser) -> list[Task]:
    query = select(Task).where(Task.owner_id == user.id).order_by(Task.created_at)
    return list(session.exec(query))


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskRead)
def create_task(data: TaskCreate, session: SessionDep, user: CurrentUser) -> Task:
    task = Task(owner_id=user.id, title=data.title.strip())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: UUID, data: TaskUpdate, session: SessionDep, user: CurrentUser) -> Task:
    task = _own_task(session, user, task_id)
    if data.title is not None:
        task.title = data.title.strip()
    if data.done is not None:
        task.done = data.done
    task.updated_at = utc_now()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, session: SessionDep, user: CurrentUser) -> None:
    task = _own_task(session, user, task_id)
    session.delete(task)
    session.commit()
