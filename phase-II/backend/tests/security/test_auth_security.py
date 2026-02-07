"""Security tests for the authentication module in the Todo Backend."""

import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from unittest.mock import patch, MagicMock
from src.auth.jwt_handler import create_access_token


@pytest.fixture
def test_client():
    """Create a test client for the API."""
    app = create_app()
    with TestClient(app) as client:
        yield client


def test_cross_user_data_access_prevention():
    """Test that a user cannot access another user's tasks."""
    app = create_app()
    client = TestClient(app)

    # Create a mock token for user 1
    user1_token_data = {"user_id": 1, "email": "user1@example.com"}
    user1_token = create_access_token(user1_token_data)

    # Try to access user 2's tasks using user 1's token
    with patch('src.api.v1.tasks.get_task_by_id') as mock_get_task:

        # Mock a task that belongs to user 2
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "User 2's Task"
        mock_task.user_id = 2  # Belongs to user 2
        mock_get_task.return_value = mock_task

        # Make request to get task with user 1's token
        response = client.get(
            "/api/tasks/1",
            headers={"Authorization": f"Bearer {user1_token}"}
        )

        # Verify access is denied (should be 404 since task won't be found for user 1)
        # In the service layer, get_task_by_id checks if task.user_id == authenticated_user_id
        assert response.status_code == 404


def test_invalid_token_rejection():
    """Test that invalid tokens are properly rejected."""
    app = create_app()
    client = TestClient(app)

    # Use an invalid/signed token
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"

    # Make request with invalid token
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )

    # Verify unauthorized response
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_malformed_authorization_header():
    """Test that malformed authorization headers are handled properly."""
    app = create_app()
    client = TestClient(app)

    # Use malformed authorization header
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "InvalidFormatToken"}
    )

    # Verify unauthorized response
    assert response.status_code == 401


def test_missing_authorization_header():
    """Test that missing authorization headers are handled properly."""
    app = create_app()
    client = TestClient(app)

    # Make request without authorization header
    response = client.get("/api/tasks")

    # Verify unauthorized response
    assert response.status_code == 401


def test_expired_token_handling():
    """Test that expired tokens are properly rejected."""
    app = create_app()
    client = TestClient(app)

    # Create an expired token by setting the exp in the past
    import time
    expired_token_data = {"user_id": 1, "email": "user@example.com", "exp": time.time() - 100}

    # We need to manually create an expired token
    from jose import jwt
    import os
    from dotenv import load_dotenv
    load_dotenv()

    secret_key = os.getenv("BETTER_AUTH_SECRET", "fallback-test-secret-key-change-in-production")
    algorithm = "HS256"

    expired_token = jwt.encode(expired_token_data, secret_key, algorithm=algorithm)

    # Make request with expired token
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    # Verify unauthorized response
    assert response.status_code == 401


def test_token_manipulation_attempts():
    """Test that manipulated tokens are properly rejected."""
    app = create_app()
    client = TestClient(app)

    # Create a valid token
    valid_token_data = {"user_id": 1, "email": "user1@example.com"}
    valid_token = create_access_token(valid_token_data)

    # Manipulate the token (change the user_id in payload without changing signature)
    # This simulates a token tampering attempt
    # Split the token to manipulate the payload
    parts = valid_token.split('.')
    # Note: Actually manipulating the JWT would require recreating the signature,
    # which would make it valid. So instead we'll test with a token that has invalid signature

    # Just create a completely invalid token with bad signature
    manipulated_token = f"{parts[0]}.{parts[1]}.invalidsignaturehere"

    # Make request with manipulated token
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {manipulated_token}"}
    )

    # Verify unauthorized response
    assert response.status_code == 401


def test_auth_bypass_attempts():
    """Test that attempts to bypass authentication fail."""
    app = create_app()
    client = TestClient(app)

    # Test using empty bearer token
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer "}
    )

    # Verify unauthorized response
    assert response.status_code == 401

    # Test using malformed token
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid-token-format"}
    )

    # Verify unauthorized response
    assert response.status_code == 401