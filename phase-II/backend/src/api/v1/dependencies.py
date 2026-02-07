"""Dependency functions for API validation in the Todo Backend."""

from fastapi import HTTPException, Path
from typing import Annotated


def validate_user_id(user_id: int = Path(..., ge=1, description="The ID of the user")) -> int:
    """Validate that user_id is a positive integer."""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer")
    return user_id


def validate_task_id(task_id: int = Path(..., ge=1, description="The ID of the task")) -> int:
    """Validate that task_id is a positive integer."""
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    return task_id


# Create annotated dependencies for reuse
UserId = Annotated[int, Path(ge=1, description="The ID of the user")]
TaskId = Annotated[int, Path(ge=1, description="The ID of the task")]