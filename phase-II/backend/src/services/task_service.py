"""Task service layer for the Todo Backend."""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select

from ..models.task import Task, TaskBase
from ..models.user import User


def create_task(session: Session, task_data: TaskBase) -> Task:
    """Create a new task in the database."""
    # Validate input data
    if not task_data.title or task_data.title.strip() == "":
        raise ValueError("Task title cannot be empty")

    # Create the task
    task = Task(**task_data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_tasks_by_user_id(session: Session, user_id: int, completed: Optional[bool] = None) -> List[Task]:
    """Get all tasks for a specific user, optionally filtered by completion status."""
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    return session.exec(query).all()


def get_task_by_id(session: Session, user_id: int, task_id: int) -> Optional[Task]:
    """Get a specific task by ID for a specific user."""
    # Get the task
    task = session.get(Task, task_id)

    # Verify task belongs to the user
    if task and task.user_id != user_id:
        return None

    return task


def update_task(session: Session, user_id: int, task_id: int, task_data: TaskBase) -> Optional[Task]:
    """Update an existing task for a specific user."""
    task = session.get(Task, task_id)

    if task and task.user_id == user_id:
        # Validate input data
        if hasattr(task_data, 'title') and task_data.title:
            if task_data.title.strip() == "":
                raise ValueError("Task title cannot be empty")

        # Update task fields
        for field, value in task_data.model_dump(exclude_unset=True).items():
            if value is not None:  # Only update if the value is provided
                setattr(task, field, value)
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    return None


def delete_task(session: Session, user_id: int, task_id: int) -> bool:
    """Delete a task for a specific user."""
    task = session.get(Task, task_id)

    if task and task.user_id == user_id:
        session.delete(task)
        session.commit()
        return True

    return False


def toggle_task_completion(session: Session, user_id: int, task_id: int) -> Optional[Task]:
    """Toggle the completion status of a task for a specific user."""
    task = session.get(Task, task_id)

    if task and task.user_id == user_id:
        # Log the completion state change
        old_completed = task.completed
        task.completed = not task.completed
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)

        # Could add additional logging here if needed
        print(f"Task {task_id} completion status changed from {old_completed} to {task.completed} for user {user_id}")
        return task

    return None