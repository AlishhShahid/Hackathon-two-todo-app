"""Logging middleware for the Todo Backend API."""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log incoming requests and outgoing responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and log details."""
        start_time = time.time()

        # Log request details
        logging.info(f"Request: {request.method} {request.url.path}")

        try:
            # Process the request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response details
            logging.info(
                f"Response: {response.status_code} "
                f"Duration: {duration:.2f}s "
                f"Path: {request.url.path} "
                f"Method: {request.method}"
            )

            return response
        except Exception as e:
            # Calculate duration for error case
            duration = time.time() - start_time

            # Log error details
            logging.error(
                f"Error: {str(e)} "
                f"Duration: {duration:.2f}s "
                f"Path: {request.url.path} "
                f"Method: {request.method}"
            )

            raise