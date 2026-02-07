# Quickstart Guide: Database & Backend Infrastructure for Todo App

## Prerequisites
- Python 3.11 or higher
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database instance
- Environment with WSL 2 (if on Windows)

## Setup Instructions

### 1. Clone and Initialize
```bash
# Navigate to project directory
cd backend

# Install dependencies
pip install -r requirements.txt
# OR if using poetry
poetry install
```

### 2. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env
```

Environment variables needed:
```
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production
```

### 3. Database Setup
```bash
# Run database migrations (if using alembic)
alembic upgrade head

# OR create tables directly with SQLModel
python -c "from backend.src.database.connection import engine; from backend.src.models import User, Task; User.metadata.create_all(engine); Task.metadata.create_all(engine)"
```

### 4. Start the Server
```bash
# Using uvicorn
uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000

# OR if using the project's main module
python -m backend.src.main
```

The server will be available at `http://localhost:8000`

## API Usage Examples

### Create a Task
```bash
curl -X POST http://localhost:8000/api/1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "due_date": "2026-02-10T10:00:00Z"
  }'
```

### List User's Tasks
```bash
curl http://localhost:8000/api/1/tasks
```

### Get Specific Task
```bash
curl http://localhost:8000/api/1/tasks/1
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries (updated)",
    "completed": true
  }'
```

### Toggle Task Completion
```bash
curl -X PATCH http://localhost:8000/api/1/tasks/1/complete
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/1/tasks/1
```

## Development Commands

### Run Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests
pytest
```

### Format Code
```bash
# Using black for formatting
black .

# Using ruff for linting
ruff check .
ruff check . --fix
```

### Database Operations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

## API Documentation
The API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Verify DATABASE_URL in environment variables
2. **Port Already in Use**: Change port in uvicorn command
3. **Missing Dependencies**: Run `pip install -r requirements.txt` again

### Environment Variables
All required environment variables are documented in `.env.example`

## Next Steps
1. Integrate authentication middleware
2. Add input validation enhancements
3. Implement proper error handling
4. Add monitoring and logging