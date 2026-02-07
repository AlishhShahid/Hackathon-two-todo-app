"""Database configuration for the Todo Backend."""

import os
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import SQLModel

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig:
    """Configuration class for database settings."""

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_backend.db")
        self.echo = os.getenv("DEBUG", "False").lower() == "true"
        self.pool_size = int(os.getenv("DB_POOL_SIZE", "5"))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))
        self.pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))

    def get_engine(self):
        """Create and return a database engine with the configured settings."""
        # SQLite doesn't support connection pooling the same way
        if self.database_url.startswith("sqlite"):
            return create_engine(
                self.database_url,
                echo=self.echo,
                connect_args={"check_same_thread": False}
            )
        # PostgreSQL with connection pooling
        return create_engine(
            self.database_url,
            echo=self.echo,
            poolclass=QueuePool,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
            pool_pre_ping=True,  # Verify connections before using
        )

    def get_database_url(self) -> str:
        """Get the database URL."""
        return self.database_url


# Create a global instance
db_config = DatabaseConfig()
engine = db_config.get_engine()


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)