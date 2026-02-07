"""Main entry point for the Todo Backend application."""

from contextlib import asynccontextmanager

import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .auth.middleware import jwt_auth

from .api.v1.tasks import router as tasks_router
from .api.v1.auth import router as auth_router
from .database.config import create_db_and_tables
# Import models to ensure they're registered with SQLModel before creating tables
from .models import User, Task  # noqa: F401
from .api.handlers import exception_handlers
from .middleware.logging_middleware import LoggingMiddleware
from .middleware.auth_logging_middleware import AuthLoggingMiddleware
from .middleware.rate_limit_middleware import RateLimitMiddleware


# Configure logging
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    print("Application starting up...")
    create_db_and_tables()
    print("Database tables created.")
    yield
    # Shutdown
    print("Application shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Todo Backend API",
        description="API for managing user tasks in the Todo application",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Add middleware (order matters - last added = first executed)
    # CORS must be last so it runs first and handles preflight requests
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(AuthLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    for exc, handler in exception_handlers.items():
        app.add_exception_handler(exc, handler)

    # Include API routers
    app.include_router(tasks_router, prefix="/api", tags=["tasks"])  # Remove user_id from prefix since authentication will handle this
    app.include_router(auth_router, prefix="/auth", tags=["auth"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Todo Backend API"}

    return app


# Create the main app instance
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        app_dir="./src"
    )