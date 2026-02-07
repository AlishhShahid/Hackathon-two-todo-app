"""Validators for API parameters in the Todo Backend."""

from fastapi import HTTPException
from typing import Union


def validate_user_id(user_id: int) -> int:
    """Validate user_id parameter."""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive integer")
    return user_id


def validate_task_id(task_id: int) -> int:
    """Validate task_id parameter."""
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Task ID must be a positive integer")
    return task_id


def validate_positive_int(value: int, field_name: str) -> int:
    """Generic validator for positive integers."""
    if value <= 0:
        raise HTTPException(status_code=400, detail=f"{field_name} must be a positive integer")
    return value