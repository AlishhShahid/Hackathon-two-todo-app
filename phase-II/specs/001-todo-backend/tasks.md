# Implementation Tasks: Database & Backend Infrastructure for Todo App

## Feature Overview
Establish a persistent backend foundation for a multi-user Todo web application by implementing the database schema and REST API infrastructure.

**Branch**: `001-todo-backend` | **Date**: 2026-02-06 | **Spec**: specs/001-todo-backend/spec.md

**Goal**: Transform the Phase I in-memory console application into a backend system with persistent storage, enabling task creation, retrieval, updating, deletion, and completion tracking for multiple users.

## Dependencies

**User Story Order**:
- Foundational components (Phase 2) must complete before user stories
- User Story 1 (P1) - Task Management Foundation - can be developed independently
- User Story 2 (P1) - Task Persistence - builds on User Story 1 foundations
- User Story 3 (P2) - Task Completion Tracking - builds on previous stories

## Parallel Execution Examples

**Within each user story phase**, tasks marked with [P] can be executed in parallel when they:
- Work on different files/modules
- Don't have direct dependencies
- Don't require sequential data setup

**Per-Story Parallelism**:
- User Story 1: Model, service, and API endpoint creation can proceed in parallel after foundational setup

## Implementation Strategy

1. **MVP Approach**: Complete User Story 1 first for basic functionality
2. **Incremental Delivery**: Each user story delivers independently testable functionality
3. **Foundation First**: Complete database setup and core infrastructure before user stories
4. **Contract-First**: API endpoints follow the OpenAPI specification in contracts/

---

## Phase 1: Setup (Project Initialization)

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 Create requirements.txt with FastAPI, SQLModel, asyncpg, uvicorn dependencies
- [X] T003 Create .env.example with DATABASE_URL and SECRET_KEY placeholders
- [X] T004 Set up project root with pyproject.toml or setup.py if using poetry
- [X] T005 Create basic directory structure: backend/src/{models,database,api,services}

## Phase 2: Foundational Components (Prerequisites for all stories)

- [X] T006 [P] Create backend/src/database/connection.py with Neon PostgreSQL connection setup
- [X] T007 [P] Create backend/src/database/__init__.py
- [X] T008 Create backend/src/models/__init__.py
- [X] T009 Create backend/src/api/__init__.py
- [X] T010 Create backend/src/services/__init__.py
- [X] T011 Create backend/src/main.py with basic FastAPI app setup
- [X] T012 [P] Create backend/tests/unit/__init__.py
- [X] T013 [P] Create backend/tests/integration/__init__.py
- [X] T014 [P] Create backend/tests/contract/__init__.py

## Phase 3: User Story 1 - Task Management Foundation (Priority: P1)

**Story Goal**: Enable users to interact with their todo tasks through a stable backend that persists their data across sessions. Allow creating, viewing, updating, deleting, and marking tasks as complete/incomplete.

**Independent Test**: Can be fully tested by creating tasks, viewing them, updating them, toggling their completion status, and deleting them - delivering the fundamental todo list functionality that users expect.

**Acceptance Scenarios**:
1. Given a user has no existing tasks, When they create a new task via the API, Then the task is stored persistently and can be retrieved later
2. Given a user has multiple tasks in their list, When they request all tasks via the API, Then all tasks are returned in a structured format
3. Given a specific task exists in the system, When the user requests that task by ID, Then only that specific task is returned

### Phase 3.1: User Story 1 - Models

- [X] T015 [P] [US1] Create backend/src/models/user.py with SQLModel User entity per data model
- [X] T016 [P] [US1] Create backend/src/models/task.py with SQLModel Task entity per data model
- [X] T017 [US1] Update backend/src/models/__init__.py to export User and Task models

### Phase 3.2: User Story 1 - Services

- [X] T018 [P] [US1] Create backend/src/services/task_service.py with CRUD operations
- [X] T019 [US1] Implement create_task function in task_service.py
- [X] T020 [US1] Implement get_tasks_by_user_id function in task_service.py
- [X] T021 [US1] Implement get_task_by_id function in task_service.py
- [X] T022 [US1] Implement update_task function in task_service.py
- [X] T023 [US1] Implement delete_task function in task_service.py
- [X] T024 [US1] Implement toggle_task_completion function in task_service.py

### Phase 3.3: User Story 1 - API Endpoints

- [X] T025 [P] [US1] Create backend/src/api/v1/__init__.py
- [X] T026 [P] [US1] Create backend/src/api/v1/tasks.py with APIRouter for task endpoints
- [X] T027 [US1] Implement POST /api/{user_id}/tasks endpoint per API contract
- [X] T028 [US1] Implement GET /api/{user_id}/tasks endpoint per API contract
- [X] T029 [US1] Implement GET /api/{user_id}/tasks/{id} endpoint per API contract
- [X] T030 [US1] Implement PUT /api/{user_id}/tasks/{id} endpoint per API contract
- [X] T031 [US1] Implement DELETE /api/{user_id}/tasks/{id} endpoint per API contract
- [X] T032 [US1] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint per API contract

### Phase 3.4: User Story 1 - API Integration

- [X] T033 [US1] Update backend/src/api/__init__.py to include task router
- [X] T034 [US1] Mount the v1 task router in backend/src/main.py
- [X] T035 [US1] Add database session dependency to FastAPI app in main.py

## Phase 4: User Story 2 - Task Persistence (Priority: P1)

**Story Goal**: Ensure users' todo tasks remain available after the application restarts or when they return later, rather than being lost like in an in-memory solution.

**Independent Test**: Can be fully tested by creating tasks, restarting the backend service, and verifying that the tasks still exist and can be retrieved.

**Acceptance Scenarios**:
1. Given a task has been created and saved, When the backend service is restarted, Then the task remains accessible and unchanged
2. Given a user has multiple tasks, When they modify a task's details, Then the changes are saved and persisted to the database

### Phase 4.1: User Story 2 - Database Configuration

- [X] T036 [P] [US2] Create backend/src/database/config.py for database configuration management
- [X] T037 [US2] Add database URL parsing and validation from environment variables
- [X] T038 [US2] Implement connection pooling configuration in database setup
- [X] T039 [US2] Create database initialization function to create all tables

### Phase 4.2: User Story 2 - Data Validation

- [X] T040 [P] [US2] Enhance User model with proper validation per data model
- [X] T041 [P] [US2] Enhance Task model with proper validation per data model
- [X] T042 [US2] Add Pydantic models for API request/response validation
- [X] T043 [US2] Update service layer with input validation before database operations

## Phase 5: User Story 3 - Task Completion Tracking (Priority: P2)

**Story Goal**: Allow users to mark tasks as complete or incomplete to track their progress and manage their workload effectively.

**Independent Test**: Can be fully tested by creating tasks, toggling their completion status, and verifying the status persists correctly.

**Acceptance Scenarios**:
1. Given a task exists with a completion status, When the user toggles the completion status via the API, Then the task's completion status is updated and persisted

### Phase 5.1: User Story 3 - Completion Logic

- [X] T044 [P] [US3] Enhance toggle_task_completion function to properly handle state transition
- [X] T045 [US3] Add proper logging for completion status changes
- [X] T046 [US3] Implement validation to ensure task completion toggle works correctly

### Phase 5.2: User Story 3 - API Enhancement

- [X] T047 [P] [US3] Add additional test coverage for completion toggle endpoint
- [X] T048 [US3] Update API documentation for PATCH /complete endpoint behavior

## Phase 6: Edge Cases & Error Handling

**Story Goal**: Handle edge cases like invalid IDs, database failures, and malformed requests.

### Phase 6.1: Error Handling

- [X] T049 [P] Create backend/src/api/exceptions.py for custom exception handling
- [X] T050 [P] Create backend/src/api/handlers.py for exception-to-response mapping
- [X] T051 [P] Add proper HTTP status codes per API contract
- [X] T052 [P] Implement validation error handling for Pydantic models
- [X] T053 Handle database connection errors gracefully
- [X] T054 Handle cases where requested task/user doesn't exist

### Phase 6.2: Validation

- [X] T055 Add validation for user_id parameter in API endpoints
- [X] T056 Add validation for task_id parameter in API endpoints
- [X] T057 Implement input sanitization for all text fields

## Phase 7: Testing & Quality Assurance

### Phase 7.1: Unit Tests

- [X] T058 [P] Create backend/tests/unit/test_models.py for model validation
- [X] T059 [P] Create backend/tests/unit/test_task_service.py for service functions
- [X] T060 [P] Create backend/tests/unit/test_validators.py for input validation
- [X] T061 [P] Write unit tests for all service layer functions

### Phase 7.2: Integration Tests

- [X] T062 [P] Create backend/tests/integration/test_api.py for API integration
- [X] T063 [P] Write tests for all CRUD endpoints following API contract
- [X] T064 Test error scenarios and edge cases
- [X] T065 Test database transaction behavior

### Phase 7.3: Contract Tests

- [X] T066 [P] Create backend/tests/contract/test_task_api_contract.py
- [X] T067 Verify API responses match OpenAPI specification
- [X] T068 Test all HTTP methods and status codes as defined in contract

## Phase 8: Polish & Cross-Cutting Concerns

### Phase 8.1: Performance & Optimization

- [X] T069 Add database indexing as specified in data model
- [X] T070 Optimize database queries for common access patterns
- [X] T071 Add request/response logging middleware
- [X] T072 Implement proper shutdown handlers for database connections

### Phase 8.2: Documentation & Setup

- [X] T073 Update backend/src/main.py with proper API documentation configuration
- [X] T074 Create alembic migration configuration in backend/alembic/
- [X] T075 Create README.md in backend/ with setup instructions
- [X] T076 Verify all components work together and backend starts successfully

### Phase 8.3: Final Validation

- [X] T077 Run all tests to verify complete functionality
- [X] T078 Test all endpoints manually via Swagger UI
- [X] T079 Verify data persists across server restarts
- [X] T080 Validate all success criteria from specification are met