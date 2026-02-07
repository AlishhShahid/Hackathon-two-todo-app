"""JWT handling utilities for the Todo Backend authentication."""

from datetime import datetime, timedelta
from typing import Optional
import os
import time
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import HTTPException, status

# Load environment variables
load_dotenv()

# Get the secret key from environment variables
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback-test-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token with the provided data."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify the JWT token and return the payload if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token is expired
        if is_token_expired(payload):
            return None

        return payload
    except JWTError:
        return None


def is_token_expired(payload: dict) -> bool:
    """Check if the token has expired based on the 'exp' claim."""
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


def decode_token_payload(token: str) -> Optional[dict]:
    """Decode the token payload without verification (for debugging purposes)."""
    try:
        # python-jose requires key even with verify_signature=False
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
        return payload
    except JWTError:
        return None


def get_current_user_id(token: str) -> Optional[int]:
    """Extract the user ID from the token."""
    payload = verify_token(token)
    if payload:
        user_id = payload.get("user_id")
        if user_id is not None:
            return int(user_id)
    return None