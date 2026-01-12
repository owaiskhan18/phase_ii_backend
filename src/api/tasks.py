from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from src.database import get_session
from src.models import Task, User
from src.dependencies import get_current_user

router = APIRouter()

# Schema for incoming Task data (creation/update)
class TaskCreate(SQLModel):
    title: str
    is_completed: bool = False

# Schema for Task response
class TaskRead(SQLModel):
    id: str
    title: str
    is_completed: bool
    user_id: str

# Schema for Task update
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None


# ------------------------
# Get all tasks
# ------------------------
@router.get("/tasks", response_model=List[TaskRead])
def read_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
    return [
        TaskRead(
            id=str(t.id),
            title=t.title,
            is_completed=t.is_completed,
            user_id=str(t.user_id)
        ) for t in tasks
    ]


# ------------------------
# Create a new task
# ------------------------
@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_task = Task(title=task.title, is_completed=task.is_completed, user_id=current_user.id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return TaskRead(
        id=str(db_task.id),
        title=db_task.title,
        is_completed=db_task.is_completed,
        user_id=str(db_task.user_id)
    )


# ------------------------
# Update a task
# ------------------------
@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskRead(
        id=str(task.id),
        title=task.title,
        is_completed=task.is_completed,
        user_id=str(task.user_id)
    )


# ------------------------
# Delete a task
# ------------------------
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
