"""Unit tests for the authentication module in the Todo Backend."""

import pytest
from unittest.mock import Mock, patch
from datetime import timedelta
from src.auth.jwt_handler import create_access_token, verify_token, get_current_user_id
from src.auth.utils import verify_password, get_password_hash


def test_create_access_token():
    """Test creating an access token with valid data."""
    data = {"user_id": 1, "email": "test@example.com"}

    token = create_access_token(data)

    # Verify token is created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_with_custom_expiry():
    """Test creating an access token with custom expiry time."""
    data = {"user_id": 1, "email": "test@example.com"}
    expiry = timedelta(minutes=60)  # 1 hour

    token = create_access_token(data, expires_delta=expiry)

    # Verify token is created
    assert token is not None
    assert isinstance(token, str)


def test_verify_valid_token():
    """Test verifying a valid token."""
    data = {"user_id": 1, "email": "test@example.com"}

    token = create_access_token(data)
    payload = verify_token(token)

    # Verify payload is returned correctly
    assert payload is not None
    assert payload["user_id"] == 1
    assert payload["email"] == "test@example.com"


def test_verify_invalid_token():
    """Test verifying an invalid token."""
    invalid_token = "invalid.token.format"

    payload = verify_token(invalid_token)

    # Verify None is returned for invalid token
    assert payload is None


def test_get_current_user_id_from_valid_token():
    """Test extracting user ID from a valid token."""
    data = {"user_id": 42, "email": "test@example.com"}

    token = create_access_token(data)
    user_id = get_current_user_id(token)

    # Verify user ID is extracted correctly
    assert user_id == 42


def test_get_current_user_id_from_invalid_token():
    """Test extracting user ID from an invalid token."""
    invalid_token = "invalid.token.format"

    user_id = get_current_user_id(invalid_token)

    # Verify None is returned for invalid token
    assert user_id is None


def test_verify_correct_password():
    """Test verifying a correct password against a hash."""
    plain_password = "correct-horse-battery-staple"
    hashed = get_password_hash(plain_password)

    result = verify_password(plain_password, hashed)

    # Verify password matches hash
    assert result is True


def test_verify_incorrect_password():
    """Test verifying an incorrect password against a hash."""
    plain_password = "correct-horse-battery-staple"
    wrong_password = "wrong-password"
    hashed = get_password_hash(plain_password)

    result = verify_password(wrong_password, hashed)

    # Verify wrong password doesn't match hash
    assert result is False


def test_get_password_hash_creates_different_hashes():
    """Test that hashing the same password creates different hashes."""
    password = "test-password"

    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Verify different hashes are created (due to salt)
    assert hash1 != hash2
    assert hash1 is not None
    assert hash2 is not None