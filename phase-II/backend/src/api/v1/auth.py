"""Authentication API endpoints for the Todo Backend."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi import Response
from fastapi.security import HTTPBearer
from sqlmodel import Session
from datetime import timedelta
from typing import Dict, Any
from ...database.connection import get_session
from ...models.user import UserBase
from ...services.auth_service import authenticate_user, create_user, get_user_by_email
from ...auth.jwt_handler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from pydantic import BaseModel


class UserLogin(BaseModel):
    """Schema for user login requests."""
    email: str
    password: str


class UserRegister(BaseModel):
    """Schema for user registration requests."""
    email: str
    password: str
    name: str = None


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    name: str = None


router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_register: UserRegister, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if user already exists
    existing_user = get_user_by_email(session, user_register.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create the user data object
    user_data = UserBase(
        email=user_register.email,
        name=user_register.name
    )

    # Create the user (this will validate password strength)
    try:
        user = create_user(session, user_data, user_register.password)
    except ValueError as e:
        # Handle password validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password validation failed: {str(e)}"
        )

    # Return user information without password
    return UserResponse(id=user.id, email=user.email, name=user.name)


@router.post("/login", response_model=TokenResponse)
def login_user(user_login: UserLogin, session: Session = Depends(get_session)):
    """Login a user and return an access token."""
    user = authenticate_user(session, user_login.email, user_login.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user(request: Request, session: Session = Depends(get_session)):
    """Get the current user based on the provided token."""
    # The user ID should be attached to the request by the middleware
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = request.state.user_id

    # Fetch user from the database
    from ...models.user import User
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(id=user.id, email=user.email, name=user.name)


@router.post("/logout")
def logout_user(response: Response):
    """Logout endpoint for token-based auth (client should just forget the token)."""
    # In a JWT-based system, there's no server-side session to destroy
    # The client should just discard the token
    # This endpoint can be used to clear any client-side storage if needed
    response.status_code = status.HTTP_200_OK
    return {"message": "Logged out successfully. Please discard your token on the client-side."}