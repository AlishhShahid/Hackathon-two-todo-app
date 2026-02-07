# Research Document: Database & Backend Infrastructure for Todo App

## Overview
This document captures all research findings for the Database & Backend Infrastructure feature. It resolves all technical unknowns and sets the foundation for implementation.

## Technology Decisions

### 1. FastAPI Framework Selection

**Decision**: Use FastAPI as the web framework for the backend
**Rationale**:
- High-performance ASGI framework with excellent async support
- Built-in automatic API documentation (Swagger UI, ReDoc)
- Strong typing support with Pydantic integration
- Production-ready and widely adopted
- Perfect for REST API development as specified

**Alternatives considered**:
- Flask: More basic, requires additional extensions for FastAPI's built-in features
- Django: Heavyweight for simple API use case
- Starlette: Lower-level, requires more boilerplate

### 2. SQLModel for ORM

**Decision**: Use SQLModel as the ORM/ODM
**Rationale**:
- Officially supported by FastAPI creator
- Combines SQLAlchemy and Pydantic features
- Supports both relational and validation models in one
- Type safety across database and API layers
- Designed for modern Python applications

**Alternatives considered**:
- Pure SQLAlchemy: Requires separate validation layer
- Tortoise ORM: Less mature than SQLModel
- Peewee: Less feature-rich than SQLModel

### 3. Neon Serverless PostgreSQL

**Decision**: Use Neon Serverless PostgreSQL as the database
**Rationale**:
- Serverless architecture fits the "stateless" architectural requirement
- PostgreSQL is robust and well-supported
- Scales automatically with demand
- Integrates well with Python ecosystem
- Supports advanced features needed for production

**Alternatives considered**:
- SQLite: Too simple for multi-user application
- MySQL: PostgreSQL offers better JSON support
- MongoDB: SQLModel designed for SQL databases

### 4. API Endpoint Structure

**Decision**: Use `/api/{user_id}/tasks` pattern for task endpoints
**Rationale**:
- Clear separation of user-specific resources
- Maintains RESTful principles
- Preps for future authentication integration
- Easy to understand and maintain

**Endpoint Design**:
- POST `/api/{user_id}/tasks` – Create task
- GET `/api/{user_id}/tasks` – List tasks
- GET `/api/{user_id}/tasks/{id}` – Get task details
- PUT `/api/{user_id}/tasks/{id}` – Update task
- DELETE `/api/{user_id}/tasks/{id}` – Delete task
- PATCH `/api/{user_id}/tasks/{id}/complete` – Toggle completion

### 5. Project Structure

**Decision**: Organize code in backend/src/ with logical modules
**Rationale**:
- Separation of concerns with dedicated folders for models, database, API, and services
- Follows common Python project patterns
- Facilitates testing and maintenance
- Enables clear architectural boundaries

**Module Breakdown**:
- `models/`: SQLModel classes for database entities
- `database/`: Connection utilities and session management
- `api/`: FastAPI route definitions
- `services/`: Business logic separated from API layer

## Best Practices Identified

### 1. Environment Configuration
- Use `.env` file for configuration
- Store database connection strings securely
- Implement proper error handling for missing configurations

### 2. Error Handling
- Implement custom exception handlers in FastAPI
- Return consistent JSON error responses
- Log errors appropriately without exposing sensitive details

### 3. Validation
- Use Pydantic models for request/response validation
- Implement input sanitization
- Validate user IDs and task IDs in endpoints

### 4. Dependency Management
- Use virtual environments
- Pin specific versions in requirements.txt
- Separate dev and prod dependencies

## Architecture Patterns

### 1. Layered Architecture
- Presentation (API routes)
- Business Logic (Services)
- Data Access (Models)
- External Systems (Database)

### 2. Session Management
- Use FastAPI's Depends for database sessions
- Implement proper session lifecycle management
- Ensure connections are closed properly

### 3. Authentication Preparation
- Design endpoints with user_id parameter for future JWT integration
- Prepare for user isolation at database level
- Structure code to accept user context from authentication middleware

## Security Considerations

### 1. Input Validation
- All API inputs validated using Pydantic
- Sanitize all user-provided content
- Prevent SQL injection through ORM usage

### 2. Error Disclosure
- Don't expose internal error details to clients
- Log full errors server-side for debugging
- Return generic error messages to users

### 3. Future Authentication Readiness
- Prepare API routes for authentication integration
- Structure data access to support user isolation
- Plan for JWT token verification