"""Exception handlers for the Todo Backend API."""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .exceptions import TodoException, UserNotFoundException, TaskNotFoundException, UnauthorizedAccessException
from ..auth.exceptions import (
    AuthenticationException,
    InvalidCredentialsException,
    TokenValidationException,
    ExpiredTokenException,
    InsufficientPermissionsException
)


async def todo_exception_handler(request: Request, exc: TodoException):
    """Handle custom Todo exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.error_code,
            "message": exc.message
        }
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    """Handle user not found exceptions."""
    return JSONResponse(
        status_code=404,
        content={
            "error": exc.error_code,
            "message": exc.message
        }
    )


async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
    """Handle task not found exceptions."""
    return JSONResponse(
        status_code=404,
        content={
            "error": exc.error_code,
            "message": exc.message
        }
    )


async def unauthorized_access_handler(request: Request, exc: UnauthorizedAccessException):
    """Handle unauthorized access exceptions."""
    return JSONResponse(
        status_code=403,
        content={
            "error": exc.error_code,
            "message": exc.message
        }
    )


async def authentication_exception_handler(request: Request, exc: AuthenticationException):
    """Handle authentication exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "AUTHENTICATION_ERROR",
            "message": exc.detail
        },
        headers=exc.headers
    )


async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    """Handle invalid credentials exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "INVALID_CREDENTIALS",
            "message": exc.detail
        },
        headers=exc.headers
    )


async def token_validation_exception_handler(request: Request, exc: TokenValidationException):
    """Handle token validation exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "TOKEN_VALIDATION_ERROR",
            "message": exc.detail
        },
        headers=exc.headers
    )


async def expired_token_exception_handler(request: Request, exc: ExpiredTokenException):
    """Handle expired token exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "TOKEN_EXPIRED",
            "message": exc.detail
        },
        headers=exc.headers
    )


async def insufficient_permissions_exception_handler(request: Request, exc: InsufficientPermissionsException):
    """Handle insufficient permissions exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "INSUFFICIENT_PERMISSIONS",
            "message": exc.detail
        },
        headers=exc.headers
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP_ERROR",
            "message": exc.detail
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation exceptions."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Validation error occurred",
            "details": exc.errors()
        }
    )


# Global exception handler registration dictionary
exception_handlers = {
    TodoException: todo_exception_handler,
    UserNotFoundException: user_not_found_handler,
    TaskNotFoundException: task_not_found_handler,
    UnauthorizedAccessException: unauthorized_access_handler,
    AuthenticationException: authentication_exception_handler,
    InvalidCredentialsException: invalid_credentials_exception_handler,
    TokenValidationException: token_validation_exception_handler,
    ExpiredTokenException: expired_token_exception_handler,
    InsufficientPermissionsException: insufficient_permissions_exception_handler,
    StarletteHTTPException: http_exception_handler,
    RequestValidationError: validation_exception_handler,
}