# Implementation Plan: Frontend UI & API Integration

**Branch**: `003-frontend-todo-ui` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-frontend-todo-ui/spec.md`

## Summary

Build a responsive Next.js frontend that enables authenticated users to manage their tasks through a centralized API client. The frontend integrates with the existing FastAPI backend (Spec 001) using JWT authentication (Spec 002) to provide CRUD operations with proper loading states, error handling, and user isolation enforcement via backend validation.

## Technical Context

**Language/Version**: TypeScript 5.x with Next.js 16+
**Primary Dependencies**: Next.js (App Router), React 18+, Better Auth client
**Storage**: N/A (frontend only; backend handles persistence)
**Testing**: Jest + React Testing Library
**Target Platform**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
**Project Type**: Web application (frontend only)
**Performance Goals**: <2s page load, <1s task creation, <500ms toggle (SC-001, SC-002, SC-003)
**Constraints**: Mobile-first responsive (320px-1024px+), 44px touch targets
**Scale/Scope**: Single-user tasks, ~100 tasks typical, no real-time sync

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Test-First | COMPLIANT | Tasks will include test specifications before implementation |
| Simplicity | COMPLIANT | No external state management; minimal dependencies |
| Library-First | N/A | Frontend feature, not library creation |
| Observability | COMPLIANT | Error states visible to users; console logging for dev |

## Project Structure

### Documentation (this feature)

```text
specs/003-frontend-todo-ui/
├── plan.md              # This file
├── research.md          # Phase 0 output - technical decisions
├── data-model.md        # Phase 1 output - TypeScript interfaces
├── quickstart.md        # Phase 1 output - setup guide
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── layout.tsx           # Root layout with AuthProvider wrapper
│   ├── page.tsx             # Landing page (redirect based on auth)
│   ├── login/
│   │   └── page.tsx         # Login page (unauthenticated users)
│   └── tasks/
│       └── page.tsx         # Main task management page (protected)
├── components/
│   ├── TaskList.tsx         # FR-008: Task list container
│   ├── TaskItem.tsx         # FR-009: Individual task with actions
│   ├── AddTaskForm.tsx      # FR-010: Task creation form
│   ├── LoadingSpinner.tsx   # FR-002: Loading indicator
│   ├── ErrorMessage.tsx     # FR-003: Error display
│   └── auth/
│       ├── LoginForm.tsx    # FR-015: Login interface
│       └── LogoutButton.tsx # FR-016: Logout control
├── lib/
│   ├── api.ts               # FR-004, FR-005, FR-006, FR-007: API client
│   └── auth-context.tsx     # FR-017: Auth state management
├── types/
│   └── index.ts             # TypeScript interfaces from data-model.md
└── tests/
    ├── components/          # Component unit tests
    └── integration/         # API integration tests
```

**Structure Decision**: Web application (Option 2 - frontend only). Backend exists in separate directory per Spec 001. This feature creates only the `frontend/` directory.

---

## Phase 1: Foundation & API Client

**Goal**: Establish project structure and centralized API communication layer.

**Covers**: FR-004, FR-005, FR-006, FR-007

### 1.1 Project Initialization

- Create Next.js application with App Router and TypeScript
- Configure environment variables for API URL
- Set up project directory structure per Source Code layout above

**Spec Mapping**: Assumptions (Next.js 16+, modern browsers)

### 1.2 TypeScript Type Definitions

- Create `/types/index.ts` with interfaces from data-model.md
- Define Task, CreateTaskRequest, UpdateTaskRequest, ApiError, AuthState types

**Spec Mapping**: Key Entities (Task, User Session, API Client)

### 1.3 Centralized API Client

- Create `/lib/api.ts` as singleton module
- Implement base fetch wrapper with:
  - Authorization header injection (FR-005)
  - 401 response detection and redirect (FR-006)
  - Error response parsing (FR-003)
- Define typed methods for all endpoints:
  - `getTasks(userId)` - GET /api/{user_id}/tasks
  - `createTask(userId, data)` - POST /api/{user_id}/tasks
  - `updateTask(userId, taskId, data)` - PUT /api/{user_id}/tasks/{id}
  - `deleteTask(userId, taskId)` - DELETE /api/{user_id}/tasks/{id}
  - `toggleComplete(userId, taskId)` - PATCH /api/{user_id}/tasks/{id}/complete

**Spec Mapping**: FR-004, FR-005, FR-006, FR-007, Success Criteria SC-004

### 1.4 API Client Tests

- Unit tests verifying:
  - Token attachment to requests
  - 401 handling triggers redirect
  - Error response parsing
  - Correct HTTP methods for each endpoint

**Spec Mapping**: FR-005, FR-006, FR-007

---

## Phase 2: Authentication Layer

**Goal**: Implement frontend authentication state management and UI.

**Covers**: FR-015, FR-016, FR-017, User Story 6

### 2.1 Authentication Context

- Create `/lib/auth-context.tsx` with AuthProvider
- Implement in-memory token storage (per research.md decision)
- Expose: isAuthenticated, token, userId, login(), logout()
- Handle token parsing to extract user ID

**Spec Mapping**: FR-017, Key Entities (User Session)

### 2.2 Protected Route Logic

- Implement route protection in layout or middleware
- Redirect unauthenticated users to /login (SC-005: <500ms)
- Redirect authenticated users from /login to /tasks

**Spec Mapping**: User Story 6 Acceptance Scenarios 1, 2

### 2.3 Login Page & Form

- Create `/app/login/page.tsx`
- Implement LoginForm component with:
  - Email/password inputs
  - Form validation
  - Loading state during submission
  - Error display for failed login
- Integrate with Better Auth for token acquisition

**Spec Mapping**: FR-015, User Story 6 Acceptance Scenarios 1, 2

### 2.4 Logout Functionality

- Create LogoutButton component
- Clear auth context on logout
- Redirect to login page

**Spec Mapping**: FR-016, User Story 6 Acceptance Scenario 3

### 2.5 Token Expiration Handling

- Detect 401 responses in API client
- Clear auth context and redirect to login
- Preserve no-data-loss behavior (graceful redirect)

**Spec Mapping**: User Story 6 Acceptance Scenario 4, Edge Cases (token expiry)

### 2.6 Authentication Tests

- Test AuthProvider state management
- Test protected route redirects
- Test login/logout flows
- Test 401 handling and redirect

**Spec Mapping**: User Story 6, FR-015, FR-016, FR-017

---

## Phase 3: Core Task Components

**Goal**: Build task display and creation UI components.

**Covers**: FR-002, FR-003, FR-008, FR-009, FR-010, FR-011, User Stories 1, 2

### 3.1 Shared UI Components

- Create LoadingSpinner component
- Create ErrorMessage component with retry button
- Ensure mobile-friendly sizing (44px touch targets)

**Spec Mapping**: FR-002, FR-003, SC-006

### 3.2 AddTaskForm Component

- Create AddTaskForm with:
  - Title input field
  - Client-side validation (non-empty title, FR-011)
  - Submit button with loading state
  - Error display for API failures
  - Form reset on successful creation

**Spec Mapping**: FR-010, FR-011, User Story 2 Acceptance Scenarios

### 3.3 TaskItem Component

- Create TaskItem displaying:
  - Task title (truncated with ellipsis for long titles)
  - Completion status indicator (checkbox/visual)
  - Edit and delete action controls
  - Loading states for individual item operations

**Spec Mapping**: FR-009, FR-012, Edge Cases (long titles)

### 3.4 TaskList Component

- Create TaskList container that:
  - Fetches tasks on mount
  - Displays loading state during fetch (FR-002)
  - Renders TaskItem for each task
  - Shows empty state for no tasks
  - Shows error state with retry for API failures

**Spec Mapping**: FR-008, User Story 1 Acceptance Scenarios

### 3.5 Task Page Integration

- Create `/app/tasks/page.tsx`
- Compose TaskList and AddTaskForm
- Pass auth context for API calls
- Responsive layout (mobile-first, desktop breakpoint at 1024px)

**Spec Mapping**: FR-001, SC-001

### 3.6 Core Component Tests

- Test AddTaskForm validation
- Test TaskItem rendering states
- Test TaskList loading/empty/error states
- Test responsive layout breakpoints

**Spec Mapping**: User Stories 1, 2, FR-001, FR-002, FR-003

---

## Phase 4: Task Interactions

**Goal**: Implement task CRUD operations and UI interactions.

**Covers**: FR-012, FR-013, FR-014, User Stories 3, 4, 5

### 4.1 Toggle Completion

- Add toggle handler to TaskItem
- Show loading state during API call
- Update UI on success
- Revert and show error on failure

**Spec Mapping**: FR-012, User Story 3 Acceptance Scenarios, SC-003

### 4.2 Inline Task Editing

- Add edit mode to TaskItem
- Show input field with current title
- Validate non-empty before save (FR-011)
- Cancel restores original value
- Show loading during save
- Show error and preserve original on failure

**Spec Mapping**: FR-013, User Story 4 Acceptance Scenarios

### 4.3 Task Deletion with Confirmation

- Add delete handler to TaskItem
- Show confirmation dialog/prompt (FR-014)
- Allow cancel to abort deletion
- Show loading during delete
- Remove from list on success
- Show error and preserve on failure

**Spec Mapping**: FR-014, User Story 5 Acceptance Scenarios

### 4.4 Interaction Tests

- Test toggle completion flow (success and error)
- Test inline editing flow (save, cancel, validation, error)
- Test deletion flow (confirm, cancel, error)

**Spec Mapping**: User Stories 3, 4, 5

---

## Phase 5: Error Handling & Edge Cases

**Goal**: Implement robust error handling and edge case behaviors.

**Covers**: Edge Cases, SC-007, SC-008

### 5.1 Network Error Handling

- Detect network failures in API client
- Display offline/error state
- Provide retry option

**Spec Mapping**: Edge Cases (network connectivity lost)

### 5.2 Backend Unavailable Handling

- Detect 500/503 responses
- Show service unavailable message
- Implement automatic retry with backoff

**Spec Mapping**: Edge Cases (backend unavailable)

### 5.3 Concurrent Edit Handling

- On update conflict (if detected), refresh task list
- Last write wins behavior
- UI reflects server state after refresh

**Spec Mapping**: Edge Cases (concurrent edits)

### 5.4 Error Message Quality

- Ensure all error states show user-friendly messages
- No technical jargon or stack traces
- Clear actionable guidance (retry, contact support)

**Spec Mapping**: SC-007

### 5.5 Edge Case Tests

- Test network failure scenarios
- Test backend unavailable scenarios
- Test error message content (no technical jargon)

**Spec Mapping**: Edge Cases, SC-007

---

## Phase 6: Responsive Design & Polish

**Goal**: Ensure responsive design meets all viewport requirements.

**Covers**: FR-001, SC-006

### 6.1 Mobile Layout (320px - 1023px)

- Stack layout for TaskList
- Full-width AddTaskForm
- Touch-friendly controls (44px minimum)
- Readable text sizes

**Spec Mapping**: FR-001, SC-006

### 6.2 Desktop Layout (1024px+)

- Optimized layout for wider viewports
- Appropriate spacing and alignment
- Maintain touch target sizes for hybrid devices

**Spec Mapping**: FR-001

### 6.3 Responsive Tests

- Visual regression tests at breakpoints
- Touch target size verification
- Layout consistency checks

**Spec Mapping**: FR-001, SC-006

---

## Requirement Coverage Matrix

| Requirement | Phase | Component/File |
|-------------|-------|----------------|
| FR-001 | 6 | All layouts |
| FR-002 | 3.1, 3.4 | LoadingSpinner, TaskList |
| FR-003 | 3.1, 5.4 | ErrorMessage |
| FR-004 | 1.3 | /lib/api.ts |
| FR-005 | 1.3 | /lib/api.ts |
| FR-006 | 1.3, 2.5 | /lib/api.ts |
| FR-007 | 1.3 | /lib/api.ts (enforced by code review) |
| FR-008 | 3.4 | TaskList |
| FR-009 | 3.3 | TaskItem |
| FR-010 | 3.2 | AddTaskForm |
| FR-011 | 3.2, 4.2 | AddTaskForm, TaskItem |
| FR-012 | 4.1 | TaskItem |
| FR-013 | 4.2 | TaskItem |
| FR-014 | 4.3 | TaskItem |
| FR-015 | 2.3 | LoginForm |
| FR-016 | 2.4 | LogoutButton |
| FR-017 | 2.1 | /lib/auth-context.tsx |

## User Story Coverage

| User Story | Priority | Phase |
|------------|----------|-------|
| US-1: View Task List | P1 | 3 |
| US-2: Create Task | P1 | 3 |
| US-3: Toggle Completion | P2 | 4 |
| US-4: Update Task | P2 | 4 |
| US-5: Delete Task | P3 | 4 |
| US-6: Authentication | P1 | 2 |

## Success Criteria Verification

| Criteria | Phase | Verification Method |
|----------|-------|---------------------|
| SC-001: <2s page load | 3.5 | Performance test |
| SC-002: <1s task creation | 3.2 | Integration test timing |
| SC-003: <500ms toggle | 4.1 | Integration test timing |
| SC-004: 100% API through client | 1.3 | Code review, linting rule |
| SC-005: <500ms login redirect | 2.2 | Integration test timing |
| SC-006: Mobile usability | 6 | Visual/manual testing |
| SC-007: User-friendly errors | 5.4 | Error message review |
| SC-008: Full lifecycle | All | End-to-end test |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better Auth integration complexity | Medium | Research phase resolved; fallback to manual JWT handling |
| Backend API changes | Low | OpenAPI contract as source of truth; adapter pattern in api.ts |
| Performance on slow networks | Medium | Loading states, pessimistic updates, error recovery |

## Next Steps

Run `/sp.tasks` to generate detailed task breakdown with test specifications.
