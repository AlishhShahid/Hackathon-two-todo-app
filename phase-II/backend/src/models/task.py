"""Task model for the Todo Backend."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import field_validator


class TaskBase(SQLModel):
    """Base class for Task model with common fields."""
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = None
    user_id: int = Field(foreign_key="user.id")

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate title is not empty and not just whitespace."""
        if not v or v.strip() == "":
            raise ValueError('Title cannot be empty')
        return v.strip()


class Task(TaskBase, table=True):
    """Task model representing a todo item that belongs to a specific user."""
    id: int = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)