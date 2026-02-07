"""Unit tests for the task service in the Todo Backend."""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from src.services.task_service import (
    create_task,
    get_tasks_by_user_id,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_completion
)
from src.models.task import TaskBase


def test_create_task_success():
    """Test successful creation of a task."""
    # Mock the session
    mock_session = Mock()
    mock_task = Mock()
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock(return_value=mock_task)

    # Prepare task data
    task_data = TaskBase(
        title="Test Task",
        description="Test Description",
        user_id=1
    )

    # Call the function
    result = create_task(mock_session, task_data)

    # Assertions
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result is not None


def test_get_tasks_by_user_id():
    """Test retrieving tasks by user ID."""
    # Mock the session
    mock_session = Mock()
    mock_exec_result = Mock()
    mock_exec_result.all = Mock(return_value=[Mock()])
    mock_session.exec = Mock(return_value=mock_exec_result)

    # Call the function
    result = get_tasks_by_user_id(mock_session, 1, None)

    # Assertions
    assert len(result) == 1
    mock_session.exec.assert_called_once()


def test_get_task_by_id_exists():
    """Test retrieving an existing task by ID."""
    # Mock the session
    mock_session = Mock()
    mock_user = Mock()
    mock_task = Mock()
    mock_session.get = Mock(side_effect=lambda cls, pk: mock_user if cls.__name__ == 'User' else mock_task)

    # Call the function
    result = get_task_by_id(mock_session, 1, 1)

    # Assertions
    assert result is not None
    assert mock_session.get.call_count == 2  # Called twice: once for user, once for task


def test_get_task_by_id_user_not_exists():
    """Test retrieving a task when user doesn't exist."""
    # Mock the session
    mock_session = Mock()
    mock_session.get = Mock(return_value=None)  # User not found

    # Call the function
    result = get_task_by_id(mock_session, 999, 1)

    # Assertions
    assert result is None


def test_update_task_success():
    """Test successful task update."""
    # Mock the session
    mock_session = Mock()
    mock_user = Mock()
    mock_task = Mock()
    mock_task.user_id = 1
    mock_session.get = Mock(side_effect=lambda cls, pk: mock_user if cls.__name__ == 'User' else mock_task)

    # Prepare task data
    task_data = TaskBase(
        title="Updated Task",
        user_id=1
    )

    # Call the function
    result = update_task(mock_session, 1, 1, task_data)

    # Assertions
    assert result is not None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_update_task_wrong_user():
    """Test updating a task that doesn't belong to the user."""
    # Mock the session
    mock_session = Mock()
    mock_user = Mock()
    mock_task = Mock()
    mock_task.user_id = 2  # Different user
    mock_session.get = Mock(side_effect=lambda cls, pk: mock_user if cls.__name__ == 'User' else mock_task)

    # Prepare task data
    task_data = TaskBase(
        title="Updated Task",
        user_id=2
    )

    # Call the function
    result = update_task(mock_session, 1, 1, task_data)

    # Assertions
    assert result is None


def test_delete_task_success():
    """Test successful task deletion."""
    # Mock the session
    mock_session = Mock()
    mock_task = Mock()
    mock_task.user_id = 1
    mock_session.get = Mock(return_value=mock_task)
    mock_session.delete = Mock()

    # Call the function
    result = delete_task(mock_session, 1, 1)

    # Assertions
    assert result is True
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_task_wrong_user():
    """Test deleting a task that doesn't belong to the user."""
    # Mock the session
    mock_session = Mock()
    mock_task = Mock()
    mock_task.user_id = 2  # Different user
    mock_session.get = Mock(return_value=mock_task)

    # Call the function
    result = delete_task(mock_session, 1, 1)

    # Assertions
    assert result is False


def test_toggle_task_completion_success():
    """Test successful task completion toggle."""
    # Mock the session
    mock_session = Mock()
    mock_user = Mock()
    mock_task = Mock()
    mock_task.user_id = 1
    mock_task.completed = False
    mock_session.get = Mock(side_effect=lambda cls, pk: mock_user if cls.__name__ == 'User' else mock_task)

    # Call the function
    result = toggle_task_completion(mock_session, 1, 1)

    # Assertions
    assert result is not None
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


def test_toggle_task_completion_unauthorized():
    """Test toggling task completion when task doesn't belong to user."""
    # Mock the session
    mock_session = Mock()
    mock_user = Mock()
    mock_task = Mock()
    mock_task.user_id = 2  # Different user
    mock_session.get = Mock(side_effect=lambda cls, pk: mock_user if cls.__name__ == 'User' else mock_task)

    # Call the function
    result = toggle_task_completion(mock_session, 1, 1)

    # Assertions
    assert result is None


def test_toggle_task_completion_user_not_found():
    """Test toggling task completion when user doesn't exist."""
    # Mock the session
    mock_session = Mock()
    mock_session.get = Mock(return_value=None)  # User not found

    # Call the function
    result = toggle_task_completion(mock_session, 999, 1)

    # Assertions
    assert result is None


def test_toggle_task_completion_task_not_found():
    """Test toggling task completion when task doesn't exist."""
    # Mock the session
    mock_session = Mock()
    mock_user = Mock()  # User exists
    mock_session.get = Mock(side_effect=[mock_user, None])  # User exists, task doesn't

    # Call the function
    result = toggle_task_completion(mock_session, 1, 999)

    # Assertions
    assert result is None


def test_toggle_task_completion_state_transition():
    """Test that completion status is properly toggled."""
    # Mock the session
    mock_session = Mock()
    mock_user = Mock()
    mock_task = Mock()
    mock_task.user_id = 1
    mock_task.completed = False  # Start as incomplete
    mock_session.get = Mock(side_effect=lambda cls, pk: mock_user if cls.__name__ == 'User' else mock_task)

    # Call the function
    result = toggle_task_completion(mock_session, 1, 1)

    # Verify the task's completion status was flipped
    assert result is not None
    # The completed property should have been toggled from False to True
    assert mock_task.completed == True  # Note: This reflects what was set during the toggle