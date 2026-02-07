# Todo Backend

Backend for the Todo Full-Stack Web Application built with FastAPI and SQLModel, featuring JWT authentication and user isolation.

## Features

- User management with secure authentication
- Task management (CRUD operations)
- Task completion tracking
- JWT-based authentication and authorization
- User isolation - each user can only access their own data
- RESTful API endpoints
- Data persistence with PostgreSQL

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLModel**: SQL databases in Python, with a focus on type hints
- **PostgreSQL**: Advanced open-source database
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the application
- **python-jose**: JWT token handling
- **passlib/bcrypt**: Password hashing
- **Better Auth**: User authentication and JWT issuance

## Authentication

The API uses JWT tokens for authentication:

1. Register a new user: `POST /auth/register`
2. Login to get a JWT token: `POST /auth/login`
3. Access protected endpoints with `Authorization: Bearer <token>` header

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and authentication secret
   ```
6. Run the application:
   ```bash
   cd src
   uvicorn main:app --reload
   ```

## API Endpoints

The API provides the following endpoints:

### Authentication Endpoints:
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Authenticate user and get JWT token
- `GET /auth/me` - Get current user information

### Task Endpoints (require authentication):
- `GET /api/tasks` - Get authenticated user's tasks
- `POST /api/tasks` - Create a new task for authenticated user
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion status

## Environment Variables

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for encryption (JWT)
- `BETTER_AUTH_SECRET`: Secret key for JWT signing and verification
- `ALGORITHM`: Algorithm for JWT encoding
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `DEBUG`: Enable/disable debug mode

## Testing

Run the tests using pytest:

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request