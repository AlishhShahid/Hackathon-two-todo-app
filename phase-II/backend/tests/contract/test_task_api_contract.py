"""
Contract tests for the API endpoints in the Todo Backend.

These tests verify that the API responses match the OpenAPI specification.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from unittest.mock import patch
from datetime import datetime


@pytest.fixture
def test_client():
    """Create a test client for the API."""
    app = create_app()
    with TestClient(app) as client:
        yield client


def test_api_response_structure_matches_contract():
    """Test that API responses match the OpenAPI specification structure."""
    app = create_app()
    client = TestClient(app)

    # Test creating a task
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.create_task') as mock_create_task:

        # Mock a user existing
        mock_get_user.return_value = type('MockUser', (), {'id': 1})()

        # Mock the task creation returning a task with the correct structure
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

        # Verify response structure matches contract
        assert response.status_code == 201
        data = response.json()

        # Check required fields from OpenAPI spec
        assert "id" in data
        assert "user_id" in data
        assert "title" in data
        assert "completed" in data
        assert "created_at" in data
        assert "updated_at" in data

        # Verify data types match contract
        assert isinstance(data["id"], int)
        assert isinstance(data["user_id"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["completed"], bool)
        assert isinstance(data["created_at"], str)  # ISO datetime string
        assert isinstance(data["updated_at"], str)  # ISO datetime string


def test_get_tasks_response_structure():
    """Test that getting tasks response matches the OpenAPI specification structure."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.get_tasks_by_user_id') as mock_get_tasks:

        # Mock a user existing and return some tasks
        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
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

        # Verify response structure matches contract
        assert response.status_code == 200
        data = response.json()

        # Should be an array of tasks
        assert isinstance(data, list)
        assert len(data) == 1

        task = data[0]
        # Check required fields from OpenAPI spec
        assert "id" in task
        assert "user_id" in task
        assert "title" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task


def test_get_specific_task_response_structure():
    """Test that getting a specific task response matches the OpenAPI specification structure."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.get_task_by_id') as mock_get_task:

        # Mock a user existing and return a task
        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
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

        # Verify response structure matches contract
        assert response.status_code == 200
        data = response.json()

        # Check required fields from OpenAPI spec
        assert "id" in data
        assert "user_id" in data
        assert "title" in data
        assert "completed" in data
        assert "created_at" in data
        assert "updated_at" in data


def test_update_task_response_structure():
    """Test that updating a task response matches the OpenAPI specification structure."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.update_task') as mock_update_task:

        # Mock a user existing and return updated task
        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
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

        # Verify response structure matches contract
        assert response.status_code == 200
        data = response.json()

        # Check required fields from OpenAPI spec
        assert "id" in data
        assert "user_id" in data
        assert "title" in data
        assert "completed" in data
        assert "created_at" in data
        assert "updated_at" in data


def test_toggle_completion_response_structure():
    """Test that toggling task completion response matches the OpenAPI specification structure."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.toggle_task_completion') as mock_toggle:

        # Mock a user existing and return toggled task
        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
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

        # Verify response structure matches contract
        assert response.status_code == 200
        data = response.json()

        # Check required fields from OpenAPI spec
        assert "id" in data
        assert "user_id" in data
        assert "title" in data
        assert "completed" in data
        assert "created_at" in data
        assert "updated_at" in data


def test_error_responses_match_contract():
    """Test that error responses match the OpenAPI specification structure."""
    app = create_app()
    client = TestClient(app)

    # Test 404 error when task not found
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.get_task_by_id') as mock_get_task:

        # Mock user exists but task doesn't
        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
        mock_get_task.return_value = None

        # Make request
        response = client.get("/api/1/tasks/999")

        # Verify error response structure matches contract
        assert response.status_code == 404


def test_http_status_codes_match_contract():
    """Test that HTTP status codes match the OpenAPI specification."""
    app = create_app()
    client = TestClient(app)

    # Test POST returns 201
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.create_task') as mock_create_task:

        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
        mock_created_task = {
            "id": 1, "title": "Test", "description": "", "completed": False,
            "user_id": 1, "created_at": "2023-01-01T00:00:00", "updated_at": "2023-01-01T00:00:00", "due_date": None
        }
        mock_create_task.return_value = mock_created_task

        response = client.post("/api/1/tasks", json={"title": "Test"})
        assert response.status_code == 201

    # Test GET returns 200
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.get_task_by_id') as mock_get_task:

        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
        mock_task = {
            "id": 1, "title": "Test", "description": "", "completed": False,
            "user_id": 1, "created_at": "2023-01-01T00:00:00", "updated_at": "2023-01-01T00:00:00", "due_date": None
        }
        mock_get_task.return_value = mock_task

        response = client.get("/api/1/tasks/1")
        assert response.status_code == 200

    # Test DELETE returns 204
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.delete_task') as mock_delete_task:

        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
        mock_delete_task.return_value = True

        response = client.delete("/api/1/tasks/1")
        assert response.status_code == 204

    # Test PATCH returns 200
    with patch('src.api.v1.tasks.session.get') as mock_get_user, \
         patch('src.services.task_service.toggle_task_completion') as mock_toggle:

        mock_get_user.return_value = type('MockUser', (), {'id': 1})()
        mock_toggled_task = {
            "id": 1, "title": "Test", "description": "", "completed": True,
            "user_id": 1, "created_at": "2023-01-01T00:00:00", "updated_at": "2023-01-01T00:00:00", "due_date": None
        }
        mock_toggle.return_value = mock_toggled_task

        response = client.patch("/api/1/tasks/1/complete")
        assert response.status_code == 200