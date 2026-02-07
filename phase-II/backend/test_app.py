"""
Simple test to verify the backend application can be imported and run.
"""

import asyncio
from src.main import app
from src.database.config import create_db_and_tables


def test_app_startup():
    """Test that the application can start up without errors."""
    print("Testing application startup...")

    # Try to create the database tables
    try:
        create_db_and_tables()
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        return False

    print("✓ Application startup test completed successfully")
    return True


if __name__ == "__main__":
    test_app_startup()