---
name: verify_jwt_token
description: "A reusable security skill for FastAPI backends. Extracts Bearer tokens, verifies the JWT signature against a shared secret, and returns the user_id for secure data filtering."
---

# JWT Token Verification

## Instructions

1. **Purpose**
   - Secure FastAPI endpoints with JWT authentication
   - Extract the Bearer token from request headers
   - Verify token signature against a shared secret
   - Return `user_id` for request-specific data filtering

2. **Setup**
   - Install JWT library: `python-jose` or `PyJWT`
   - Define a secure secret key and algorithm
   - Create a reusable FastAPI dependency for token verification

3. **Implementation Steps**
   - Extract `Authorization` header from request
   - Remove "Bearer " prefix
   - Decode JWT using the secret key and algorithm
   - Validate token payload and extract `user_id`
   - Raise `HTTPException(401)` for invalid or expired tokens
   - Return `user_id` to be used in endpoint queries

## Best Practices
- Always validate the presence of `Authorization` header
- Use secure algorithms (HS256 or RS256)
- Keep secret keys safe and rotate periodically
- Log failed authentication attempts
- Use this as a dependency (`Depends`) in endpoints to enforce user isolation

## Example Structure
```python
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Config
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Extracts and verifies JWT token from Authorization header.
    Returns the user_id for request filtering.
    Raises HTTP 401 if token is invalid.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Usage in an endpoint
@app.get("/secure-data")
def get_secure_data(current_user: int = Depends(verify_jwt_token)):
    # current_user contains the authenticated user's ID
    return {"user_id": current_user, "data": "This is secured data"}
