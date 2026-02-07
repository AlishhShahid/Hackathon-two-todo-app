"""Pydantic models for API request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class CreateTaskRequest(BaseModel):
    """Request model for creating a new task."""
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate title is not empty."""
        if not v or v.strip() == "":
            raise ValueError('Title cannot be empty')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        """Validate description if provided."""
        if v is not None:
            v = v.strip()
            if len(v) > 1000:
                raise ValueError('Description cannot exceed 1000 characters')
        return v


class UpdateTaskRequest(BaseModel):
    """Request model for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def validate_update_title(cls, v):
        """Validate title if provided."""
        if v is not None:
            v = v.strip()
            if v == "":
                raise ValueError('Title cannot be empty')
        return v

    @field_validator('description')
    @classmethod
    def validate_update_description(cls, v):
        """Validate description if provided."""
        if v is not None:
            v = v.strip()
            if len(v) > 1000:
                raise ValueError('Description cannot exceed 1000 characters')
        return v


class TaskResponse(BaseModel):
    """Response model for task data."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    error: str
    message: str