"""Custom exceptions for the Todo Backend API."""


class TodoException(Exception):
    """Base exception class for Todo application errors."""

    def __init__(self, message: str, error_code: str = "GENERAL_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UserNotFoundException(TodoException):
    """Raised when a user is not found."""

    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} not found", "USER_NOT_FOUND")


class TaskNotFoundException(TodoException):
    """Raised when a task is not found."""

    def __init__(self, task_id: int):
        super().__init__(f"Task with ID {task_id} not found", "TASK_NOT_FOUND")


class UnauthorizedAccessException(TodoException):
    """Raised when a user attempts to access a resource they don't own."""

    def __init__(self):
        super().__init__("Unauthorized access to resource", "UNAUTHORIZED_ACCESS")