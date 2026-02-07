# Data Model: Frontend UI & API Integration

**Feature Branch**: `003-frontend-todo-ui`
**Date**: 2026-02-06

## Frontend TypeScript Interfaces

### Task Entity

Represents a user's todo item as received from and sent to the backend API.

```typescript
interface Task {
  id: number;
  user_id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;  // ISO 8601 datetime
  updated_at: string;  // ISO 8601 datetime
  due_date?: string;   // ISO 8601 datetime (optional)
}
```

**Source**: `specs/001-todo-backend/contracts/openapi.yaml` - Task schema

### Task Request DTOs

```typescript
interface CreateTaskRequest {
  title: string;          // Required, max 255 chars
  description?: string;   // Optional
  due_date?: string;      // Optional ISO 8601 datetime
}

interface UpdateTaskRequest {
  title?: string;         // Optional, max 255 chars
  description?: string;   // Optional
  due_date?: string;      // Optional ISO 8601 datetime
}
```

### API Error Response

```typescript
interface ApiError {
  error: string;    // Error code
  message: string;  // Human-readable message
}
```

### Authentication State

```typescript
interface AuthState {
  isAuthenticated: boolean;
  token: string | null;      // JWT token (in-memory only)
  userId: number | null;     // Extracted from token
  userEmail: string | null;  // Extracted from token
}
```

### UI State Types

```typescript
type LoadingState = 'idle' | 'loading' | 'success' | 'error';

interface TaskListState {
  tasks: Task[];
  loadingState: LoadingState;
  error: string | null;
}

interface TaskItemState {
  isEditing: boolean;
  isToggling: boolean;
  isDeleting: boolean;
  editError: string | null;
}
```

## Entity Relationships

```
┌─────────────────┐
│   AuthContext   │
│  (Global State) │
├─────────────────┤
│ token           │───────┐
│ userId          │       │
│ isAuthenticated │       │
└─────────────────┘       │
                          │ provides token
                          ▼
┌─────────────────┐     ┌─────────────────┐
│   API Client    │────▶│  Backend API    │
│  (/lib/api.ts)  │     │  (FastAPI)      │
└─────────────────┘     └─────────────────┘
        │                       │
        │ fetches               │ returns
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│    TaskList     │◀────│    Task[]       │
│   Component     │     │   (JSON)        │
└─────────────────┘     └─────────────────┘
        │
        │ renders
        ▼
┌─────────────────┐
│    TaskItem     │
│   Component     │
└─────────────────┘
```

## Validation Rules

| Field | Rule | Source |
|-------|------|--------|
| `Task.title` | Required, max 255 characters | FR-011, OpenAPI |
| `Task.title` | Non-empty string | FR-011 |
| `CreateTaskRequest.title` | Required | OpenAPI |
| `UpdateTaskRequest.title` | Optional but non-empty if provided | FR-011 |

## State Transitions

### Task Lifecycle

```
[Not Exists] ──create──▶ [Active/Incomplete]
                              │
                              │ toggle
                              ▼
                         [Completed]
                              │
                              │ toggle
                              ▼
                         [Active/Incomplete]
                              │
                              │ delete
                              ▼
                         [Not Exists]
```

### Authentication State

```
[Unauthenticated] ──login──▶ [Authenticated]
                                   │
                                   │ logout / token expires
                                   ▼
                             [Unauthenticated]
```

## API Endpoint Mapping

| Frontend Action | API Endpoint | Method |
|-----------------|--------------|--------|
| List tasks | `/api/{user_id}/tasks` | GET |
| Create task | `/api/{user_id}/tasks` | POST |
| Update task | `/api/{user_id}/tasks/{id}` | PUT |
| Delete task | `/api/{user_id}/tasks/{id}` | DELETE |
| Toggle completion | `/api/{user_id}/tasks/{id}/complete` | PATCH |

**Note**: `user_id` is extracted from JWT token by the backend. Frontend includes it in API calls but backend validates against authenticated user.
