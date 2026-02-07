"""Authentication middleware for the Todo Backend."""

from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import verify_token, validate_token_payload
from .exceptions import TokenValidationException, ExpiredTokenException


class JWTAuth:
    """JWT authentication class to handle token validation."""

    def __init__(self):
        self.scheme = HTTPBearer(auto_error=True)

    async def __call__(self, request: Request):
        # Extract the authorization header
        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            raise TokenValidationException("No authorization header provided")

        # Check if the header has the correct format: "Bearer <token>"
        if not authorization_header.startswith("Bearer "):
            raise TokenValidationException("Invalid authorization header format. Expected 'Bearer <token>'")

        # Extract the token
        token = authorization_header[len("Bearer "):]

        # Verify the token
        payload = verify_token(token)
        if payload is None:
            # Check if it's expired separately to give a more specific error
            from .jwt_handler import decode_token_payload as decode_payload
            temp_payload = decode_payload(token)
            if temp_payload and 'exp' in temp_payload:
                import time
                if temp_payload['exp'] < time.time():
                    raise ExpiredTokenException("Token has expired")

            raise TokenValidationException("Invalid or expired token")

        # Validate the token payload contains required claims
        if not validate_token_payload(payload):
            raise TokenValidationException("Invalid token payload: missing required claims")

        # Add the user ID to the request state for use in endpoints
        request.state.user_id = payload.get("user_id")
        return payload


# Create an instance of the JWT authentication class
jwt_auth = JWTAuth()