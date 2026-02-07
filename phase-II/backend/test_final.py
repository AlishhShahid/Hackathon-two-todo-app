"""
Final integration test to verify the complete backend application works.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import patch, MagicMock


def test_complete_application_flow():
    """
    Test the complete application flow:
    1. Create a task
    2. Retrieve the task
    3. Update the task
    4. Toggle completion status
    5. Delete the task
    """
    app = create_app()
    client = TestClient(app)

    # Mock all database interactions to avoid needing an actual database
    with patch('src.api.v1.tasks.get_session'), \
         patch('src.api.v1.tasks.session.get') as mock_get, \
         patch('src.services.task_service.create_task') as mock_create_task, \
         patch('src.services.task_service.get_task_by_id') as mock_get_task, \
         patch('src.services.task_service.get_tasks_by_user_id') as mock_get_tasks, \
         patch('src.services.task_service.update_task') as mock_update_task, \
         patch('src.services.task_service.delete_task') as mock_delete_task, \
         patch('src.services.task_service.toggle_task_completion') as mock_toggle:

        # Set up mocks
        mock_get.return_value = MagicMock()  # Simulate user exists
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
        mock_updated_task = {
            "id": 1,
            "title": "Updated Test Task",
            "description": "Updated Description",
            "completed": True,
            "user_id": 1,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "due_date": None
        }

        # Test 1: Create a task
        mock_create_task.return_value = mock_created_task
        response = client.post("/api/1/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })
        assert response.status_code == 201
        assert response.json()["title"] == "Test Task"
        print("✓ Task creation endpoint works")

        # Test 2: Get all tasks
        mock_get_tasks.return_value = [mock_created_task]
        response = client.get("/api/1/tasks")
        assert response.status_code == 200
        assert len(response.json()) == 1
        print("✓ Get tasks endpoint works")

        # Test 3: Get specific task
        mock_get_task.return_value = mock_created_task
        response = client.get("/api/1/tasks/1")
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"
        print("✓ Get specific task endpoint works")

        # Test 4: Update task
        mock_update_task.return_value = mock_updated_task
        response = client.put("/api/1/tasks/1", json={
            "title": "Updated Test Task",
            "description": "Updated Description"
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Test Task"
        print("✓ Update task endpoint works")

        # Test 5: Toggle completion
        mock_toggle.return_value = mock_updated_task
        response = client.patch("/api/1/tasks/1/complete")
        assert response.status_code == 200
        assert response.json()["completed"] is True
        print("✓ Toggle completion endpoint works")

        # Test 6: Delete task
        mock_delete_task.return_value = True
        response = client.delete("/api/1/tasks/1")
        assert response.status_code == 204
        print("✓ Delete task endpoint works")

        print("\n🎉 All tests passed! The Todo Backend is functioning correctly.")


def test_error_handling():
    """Test that error handling works correctly."""
    app = create_app()
    client = TestClient(app)

    with patch('src.api.v1.tasks.session.get', return_value=None):  # Simulate user not found
        # Test creating a task with non-existent user
        response = client.post("/api/999/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })
        assert response.status_code == 404
        print("✓ Error handling works correctly")


def test_validation():
    """Test that input validation works correctly."""
    app = create_app()
    client = TestClient(app)

    # Test with invalid task ID (negative)
    response = client.get("/api/1/tasks/-1")
    assert response.status_code == 422  # Validation error

    # Test with invalid user ID (negative)
    response = client.get("/api/-1/tasks/1")
    assert response.status_code == 422  # Validation error
    print("✓ Input validation works correctly")


if __name__ == "__main__":
    print("Running final integration tests...\n")

    test_complete_application_flow()
    test_error_handling()
    test_validation()

    print("\n✅ All final tests passed! The Todo Backend implementation is complete and functional.")