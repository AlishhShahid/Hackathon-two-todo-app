"""Integration tests for database transactions in the Todo Backend."""

import pytest
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import patch
from src.models.user import User
from src.models.task import Task
from src.services.task_service import create_task, get_task_by_id


def test_database_transaction_commit():
    """Test that database transactions commit successfully."""
    # This is a unit-style test that simulates database transactions
    # In a real implementation, this would connect to an actual database

    # Mock a session
    mock_session = Session(bind=create_engine("sqlite:///:memory:"))

    # Create tables in the mock database
    SQLModel.metadata.create_all(bind=mock_session.bind)

    # Add a user
    user = User(
        email="test@example.com",
        password_hash="hash123",
        first_name="Test",
        last_name="User"
    )
    mock_session.add(user)
    mock_session.commit()

    # Create a task for this user
    from src.models.task import TaskBase
    task_data = TaskBase(
        title="Test Transaction Task",
        description="Test transaction description",
        user_id=user.id
    )

    # Test create_task function
    created_task = create_task(mock_session, task_data)

    # Verify the task was created
    assert created_task.title == "Test Transaction Task"
    assert created_task.user_id == user.id

    # Verify we can retrieve the task
    retrieved_task = mock_session.get(Task, created_task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Transaction Task"


def test_database_transaction_rollback():
    """Test that database transactions rollback on error."""
    # Mock a session
    mock_session = Session(bind=create_engine("sqlite:///:memory:"))

    # Create tables in the mock database
    SQLModel.metadata.create_all(bind=mock_session.bind)

    # Add a user
    user = User(
        email="test@example.com",
        password_hash="hash123",
        first_name="Test",
        last_name="User"
    )
    mock_session.add(user)
    mock_session.commit()

    # Try to create a task with invalid data (this should fail)
    from src.models.task import TaskBase
    task_data = TaskBase(
        title="",  # Empty title should cause validation error
        user_id=user.id
    )

    # Attempt to create task and expect an error
    try:
        create_task(mock_session, task_data)
        # If we reach this line, the test should fail
        assert False, "Expected validation error was not raised"
    except ValueError:
        # Expected error occurred
        pass

    # Verify no tasks were created in the session
    from sqlmodel import select
    tasks = mock_session.exec(select(Task)).all()
    assert len(tasks) == 0


def test_multiple_database_operations():
    """Test multiple database operations in sequence."""
    # Mock a session
    mock_session = Session(bind=create_engine("sqlite:///:memory:"))

    # Create tables in the mock database
    SQLModel.metadata.create_all(bind=mock_session.bind)

    # Add a user
    user = User(
        email="test@example.com",
        password_hash="hash123",
        first_name="Test",
        last_name="User"
    )
    mock_session.add(user)
    mock_session.commit()

    # Create multiple tasks
    from src.models.task import TaskBase
    titles = ["Task 1", "Task 2", "Task 3"]

    for title in titles:
        task_data = TaskBase(
            title=title,
            description=f"Description for {title}",
            user_id=user.id
        )
        created_task = create_task(mock_session, task_data)
        assert created_task.title == title

    # Verify all tasks were created
    from sqlmodel import select
    tasks = mock_session.exec(select(Task)).all()
    assert len(tasks) == 3

    # Verify each task belongs to the correct user
    for task in tasks:
        assert task.user_id == user.id