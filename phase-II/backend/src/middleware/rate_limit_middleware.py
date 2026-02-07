"""Rate limiting middleware for authentication endpoints."""

import time
from collections import defaultdict, deque
from typing import Callable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware that limits requests based on IP address.
    """

    def __init__(self, app, requests_per_minute: int = 10, auth_requests_per_minute: int = 5):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.auth_requests_per_minute = auth_requests_per_minute
        # Store request timestamps per IP address
        self.requests = defaultdict(deque)

    def is_limited(self, client_ip: str, endpoint: str, max_requests: int) -> bool:
        """Check if a client is rate limited."""
        now = time.time()
        # Remove requests older than 1 minute
        while self.requests[client_ip] and self.requests[client_ip][0] < now - 60:
            self.requests[client_ip].popleft()

        # Check if too many requests
        if len(self.requests[client_ip]) >= max_requests:
            return True

        # Add current request
        self.requests[client_ip].append(now)
        return False

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        # Apply different rate limits based on endpoint
        if path.startswith('/auth'):
            max_requests = self.auth_requests_per_minute
        else:
            max_requests = self.requests_per_minute

        if self.is_limited(client_ip, path, max_requests):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )

        response = await call_next(request)
        return response