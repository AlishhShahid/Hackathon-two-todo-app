"""Integration tests for the API endpoints in the Todo Backend."""

import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from sqlmodel import create_engine, Session, SQLModel
from src.database.config import db_config
from unittest.mock import patch


@pytest.fixture
def test_client():
    """Create a test client for the API."""
    app = create_app()
    with TestClient(app) as client:
        yield client


def test_root_endpoint(test_client):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to the Todo Backend API"


def test_create_task_endpoint():
    """Test creating a new task via the API."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations to avoid needing actual DB
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.create_task') as mock_create_task:

        # Mock a user existing
        mock_get_user.return_value = {"id": 1}

        # Mock the task creation returning a task
        mock_created_task = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": False,
            "user_id": 1,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "due_date": None
        }
        mock_create_task.return_value = mock_created_task

        # Make request
        response = client.post("/api/1/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })

        assert response.status_code == 201
        assert response.json()["title"] == "Test Task"


def test_get_tasks_endpoint():
    """Test getting tasks for a user via the API."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.get_tasks_by_user_id') as mock_get_tasks:

        # Mock a user existing and return some tasks
        mock_get_user.return_value = {"id": 1}
        mock_tasks = [{
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": False,
            "user_id": 1,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "due_date": None
        }]
        mock_get_tasks.return_value = mock_tasks

        # Make request
        response = client.get("/api/1/tasks")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["title"] == "Test Task"


def test_get_specific_task_endpoint():
    """Test getting a specific task via the API."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.get_task_by_id') as mock_get_task:

        # Mock a user existing and return a task
        mock_get_user.return_value = {"id": 1}
        mock_task = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": False,
            "user_id": 1,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "due_date": None
        }
        mock_get_task.return_value = mock_task

        # Make request
        response = client.get("/api/1/tasks/1")

        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"


def test_update_task_endpoint():
    """Test updating a task via the API."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.update_task') as mock_update_task:

        # Mock a user existing and return updated task
        mock_get_user.return_value = {"id": 1}
        mock_updated_task = {
            "id": 1,
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True,
            "user_id": 1,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "due_date": None
        }
        mock_update_task.return_value = mock_updated_task

        # Make request
        response = client.put("/api/1/tasks/1", json={
            "title": "Updated Task",
            "completed": True
        })

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Task"
        assert response.json()["completed"] is True


def test_delete_task_endpoint():
    """Test deleting a task via the API."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.delete_task') as mock_delete_task:

        # Mock a user existing
        mock_get_user.return_value = {"id": 1}
        mock_delete_task.return_value = True

        # Make request
        response = client.delete("/api/1/tasks/1")

        assert response.status_code == 204  # No content


def test_toggle_task_completion_endpoint():
    """Test toggling task completion via the API."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.toggle_task_completion') as mock_toggle:

        # Mock a user existing and return toggled task
        mock_get_user.return_value = {"id": 1}
        mock_toggled_task = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": True,
            "user_id": 1,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "due_date": None
        }
        mock_toggle.return_value = mock_toggled_task

        # Make request
        response = client.patch("/api/1/tasks/1/complete")

        assert response.status_code == 200
        assert response.json()["completed"] is True