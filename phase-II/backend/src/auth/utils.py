"""Authentication utilities for the Todo Backend."""

import bcrypt
from datetime import datetime, timedelta
import os
from typing import Optional
from jose import JWTError
import re


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token with the provided data."""
    from .jwt_handler import create_access_token as handler_create_token
    return handler_create_token(data, expires_delta)


def verify_token(token: str) -> Optional[dict]:
    """Verify the JWT token and return the payload if valid."""
    from .jwt_handler import verify_token as handler_verify_token
    return handler_verify_token(token)


def get_current_user_id_from_token(token: str) -> Optional[int]:
    """Extract the user ID from the token."""
    from .jwt_handler import get_current_user_id
    return get_current_user_id(token)


def is_token_expired(payload: dict) -> bool:
    """Check if the token has expired based on the 'exp' claim."""
    import time
    exp = payload.get("exp")
    if exp is None:
        return False
    return time.time() >= exp


def validate_token_payload(payload: dict) -> bool:
    """Validate that the token payload contains required claims."""
    required_claims = ["user_id", "exp"]
    for claim in required_claims:
        if claim not in payload:
            return False
    return True


def get_user_id_from_payload(payload: dict) -> Optional[int]:
    """Extract user ID from token payload."""
    user_id = payload.get("user_id")
    if user_id is not None:
        return int(user_id)
    return None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength and return (is_valid, reason)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"

    return True, "Password is strong"