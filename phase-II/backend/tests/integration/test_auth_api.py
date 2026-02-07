"""Integration tests for the authentication API endpoints in the Todo Backend."""

import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from unittest.mock import patch, MagicMock
from src.models.user import User


@pytest.fixture
def test_client():
    """Create a test client for the API."""
    app = create_app()
    with TestClient(app) as client:
        yield client


def test_register_user_endpoint():
    """Test registering a new user via the API."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.services.auth_service.get_user_by_email') as mock_get_user, \
         patch('src.services.auth_service.create_user') as mock_create_user:

        # Mock that user doesn't exist yet
        mock_get_user.return_value = None

        # Mock the created user
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.name = "Test User"
        mock_create_user.return_value = mock_user

        # Make request
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "securepassword123",
            "name": "Test User"
        })

        # Verify response
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"


def test_register_existing_user_fails():
    """Test that registering an existing user fails."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.services.auth_service.get_user_by_email') as mock_get_user:

        # Mock that user already exists
        mock_existing_user = MagicMock()
        mock_existing_user.id = 1
        mock_get_user.return_value = mock_existing_user

        # Make request
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "securepassword123",
            "name": "Test User"
        })

        # Verify response
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]


def test_login_user_success():
    """Test successful user login."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.services.auth_service.authenticate_user') as mock_authenticate:

        # Mock successful authentication
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_authenticate.return_value = mock_user

        # Make request
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "correctpassword"
        })

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


def test_login_user_failure():
    """Test failed user login with wrong credentials."""
    app = create_app()
    client = TestClient(app)

    # Mock database operations
    with patch('src.services.auth_service.authenticate_user') as mock_authenticate:

        # Mock failed authentication
        mock_authenticate.return_value = None

        # Make request
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })

        # Verify response
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]


def test_auth_required_endpoint_without_token():
    """Test that endpoints requiring authentication return 401 without token."""
    app = create_app()
    client = TestClient(app)

    # Make request without token to a protected endpoint
    response = client.get("/auth/me")

    # Verify unauthorized response
    assert response.status_code == 401


def test_protected_task_endpoints_require_authentication():
    """Test that task endpoints require authentication."""
    app = create_app()
    client = TestClient(app)

    # Make request without token to a protected task endpoint
    response = client.get("/api/tasks")

    # Verify unauthorized response
    assert response.status_code == 401


def test_get_current_user_endpoint():
    """Test the get current user endpoint."""
    app = create_app()
    client = TestClient(app)

    # This would require mocking the authentication middleware to work properly
    # For now, we'll just test that it requires authentication
    response = client.get("/auth/me")

    # Verify unauthorized response
    assert response.status_code == 401