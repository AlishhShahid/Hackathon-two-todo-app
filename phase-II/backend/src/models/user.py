"""User model for the Todo Backend."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import field_validator
import re


class UserBase(SQLModel):
    """Base class for User model with common fields."""
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v.lower().strip()


class User(UserBase, table=True):
    """User model representing a registered user in the system."""
    id: int = Field(primary_key=True, nullable=False)
    hashed_password: str = Field(nullable=False)  # Password hash should not be empty
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)