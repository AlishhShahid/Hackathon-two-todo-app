"""API endpoints for task management in the Todo Backend."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi import Path
from typing import Annotated
from sqlmodel import Session
from typing import List, Optional

from ...database.connection import get_session
from ...models.task import Task
from ...models.user import User
from .models import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from ...services.task_service import (
    create_task,
    get_tasks_by_user_id,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_completion
)
from ...auth.middleware import jwt_auth

router = APIRouter(dependencies=[Depends(jwt_auth)])


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    request: Request,
    task_data: CreateTaskRequest,
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user."""
    # Get authenticated user ID from the request state
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    authenticated_user_id = request.state.user_id

    # Verify user exists
    user = session.get(User, authenticated_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a TaskBase-like object from the validated request data
    from ...models.task import TaskBase
    task_base = TaskBase(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        user_id=authenticated_user_id
    )

    try:
        task = create_task(session, task_base)
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks", response_model=List[TaskResponse])
def get_user_tasks(
    request: Request,
    completed: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    """Get all tasks for the authenticated user, optionally filtered by completion status."""
    # Get authenticated user ID from the request state
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    authenticated_user_id = request.state.user_id

    # Verify user exists
    user = session.get(User, authenticated_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tasks = get_tasks_by_user_id(session, authenticated_user_id, completed)
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_specific_task(
    request: Request,
    task_id: Annotated[int, Path(ge=1, description="The ID of the task")],
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for the authenticated user."""
    # Get authenticated user ID from the request state
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    authenticated_user_id = request.state.user_id

    # Verify user exists
    user = session.get(User, authenticated_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = get_task_by_id(session, authenticated_user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_existing_task(
    request: Request,
    task_id: Annotated[int, Path(ge=1, description="The ID of the task")],
    task_data: UpdateTaskRequest,
    session: Session = Depends(get_session)
):
    """Update an existing task for the authenticated user."""
    # Get authenticated user ID from the request state
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    authenticated_user_id = request.state.user_id

    # Verify user exists
    user = session.get(User, authenticated_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a TaskBase-like object from the validated request data
    from ...models.task import TaskBase
    task_base = TaskBase(
        title=task_data.title or "",
        description=task_data.description,
        due_date=task_data.due_date,
        user_id=authenticated_user_id
    )

    task = update_task(session, authenticated_user_id, task_id, task_base)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(
    request: Request,
    task_id: int,
    session: Session = Depends(get_session)
):
    """Delete a task for the authenticated user."""
    # Get authenticated user ID from the request state
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    authenticated_user_id = request.state.user_id

    # Verify user exists
    user = session.get(User, authenticated_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = delete_task(session, authenticated_user_id, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_completion_status(
    request: Request,
    task_id: int,
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task for the authenticated user."""
    # Get authenticated user ID from the request state
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    authenticated_user_id = request.state.user_id

    # Verify user exists
    user = session.get(User, authenticated_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = toggle_task_completion(session, authenticated_user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not owned by user")
    return task