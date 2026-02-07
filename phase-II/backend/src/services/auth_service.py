"""Authentication service layer for the Todo Backend."""

from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from ..models.user import User
from ..models.user import UserBase
from ..auth.jwt_handler import create_access_token
from ..auth.utils import verify_password, get_password_hash, validate_password_strength


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    # Find the user by email
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    # Verify user exists and password is correct
    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


def create_user(session: Session, user_data: UserBase, password: str) -> User:
    """Create a new user with the provided data and password."""
    # Validate password strength
    is_valid, reason = validate_password_strength(password)
    if not is_valid:
        raise ValueError(reason)

    # Hash the password
    hashed_password = get_password_hash(password)

    # Create the user object
    user = User(
        email=user_data.email,
        name=user_data.name,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password
    )

    # Add to session and commit
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by their email address."""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def create_access_token_for_user(user_id: int, expires_delta: Optional[timedelta] = None):
    """Create an access token for a specific user."""
    data = {"user_id": user_id}
    return create_access_token(data, expires_delta)