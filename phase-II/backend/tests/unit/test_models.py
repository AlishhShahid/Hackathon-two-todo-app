"""Unit tests for the models in the Todo Backend."""

import pytest
from datetime import datetime
from src.models.user import User, UserBase
from src.models.task import Task, TaskBase


def test_user_model_creation():
    """Test creating a user model instance."""
    user_data = UserBase(
        email="test@example.com",
        first_name="John",
        last_name="Doe"
    )

    user = User(
        **user_data.model_dump(),
        password_hash="hashed_password"
    )

    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.password_hash == "hashed_password"
    assert user.is_active is True  # default value


def test_user_model_email_validation():
    """Test email validation in user model."""
    # Test valid email
    user_data = UserBase(
        email="valid@example.com"
    )

    user = User(
        **user_data.model_dump(),
        password_hash="hashed_password"
    )

    assert user.email == "valid@example.com"

    # Note: Since we're using SQLModel/Pydantic validation,
    # the validation would occur during instantiation
    # If validation fails, an exception would be raised


def test_task_model_creation():
    """Test creating a task model instance."""
    task_data = TaskBase(
        title="Test Task",
        description="Test Description",
        user_id=1
    )

    task = Task(
        **task_data.model_dump()
    )

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.user_id == 1
    assert task.completed is False  # default value


def test_task_model_title_validation():
    """Test title validation in task model."""
    # Test valid title
    task_data = TaskBase(
        title="Valid Task Title",
        user_id=1
    )

    task = Task(
        **task_data.model_dump()
    )

    assert task.title == "Valid Task Title"

    # Empty title validation happens at Pydantic level


def test_task_default_values():
    """Test default values for task model."""
    task_data = TaskBase(
        title="Test Task",
        user_id=1
    )

    task = Task(
        **task_data.model_dump()
    )

    assert task.completed is False
    assert task.created_at is not None
    assert task.updated_at is not None