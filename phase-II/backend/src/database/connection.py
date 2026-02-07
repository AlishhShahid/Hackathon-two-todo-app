"""Database connection setup for the Todo Backend."""

from sqlmodel import Session
from typing import Generator

from .config import engine


def get_session() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:
        yield session