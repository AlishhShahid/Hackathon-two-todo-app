"""Authentication logging middleware for the Todo Backend."""

import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class AuthLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log authentication-related events."""

    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)

        # Set up logging configuration
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get the endpoint path
        path = request.url.path
        method = request.method

        # Log authentication-related requests
        if path.startswith('/auth'):
            client_host = request.client.host if request.client else "unknown"
            self.logger.info(f"Authentication request: {method} {path} from {client_host}")

            # For login attempts, log user email (without storing password)
            if path == '/auth/login' and method == 'POST':
                try:
                    body_bytes = await request.body()
                    import json
                    body = json.loads(body_bytes.decode('utf-8'))
                    email = body.get('email', 'unknown')
                    self.logger.info(f"Login attempt for user: {email}")
                except:
                    # If we can't read the body (e.g., streaming request), continue without logging email
                    pass

        # Process the request
        response = await call_next(request)

        # Log authentication responses
        if path.startswith('/auth'):
            client_host = request.client.host if request.client else "unknown"
            self.logger.info(f"Authentication response: {method} {path} - Status {response.status_code} from {client_host}")

            if path == '/auth/login' and method == 'POST':
                if response.status_code == 200:
                    self.logger.info(f"Successful login from {client_host}")
                elif response.status_code == 401:
                    self.logger.warning(f"Failed login attempt from {client_host}")

        return response