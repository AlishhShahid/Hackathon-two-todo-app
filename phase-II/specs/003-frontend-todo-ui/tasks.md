# Tasks: Frontend UI & API Integration

**Input**: Design documents from `/specs/003-frontend-todo-ui/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Not explicitly requested - test tasks excluded per template guidance.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` at repository root (backend exists separately per Spec 001)

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Project initialization and basic structure

- [x] T001 Create Next.js application with App Router and TypeScript in frontend/
- [x] T002 Configure environment variables with NEXT_PUBLIC_API_URL in frontend/.env.local
- [x] T003 [P] Create project directory structure per plan.md in frontend/
- [x] T004 [P] Configure TypeScript and ESLint settings in frontend/tsconfig.json and frontend/.eslintrc.json

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETE

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create TypeScript interfaces for Task, CreateTaskRequest, UpdateTaskRequest in frontend/types/index.ts
- [x] T006 [P] Create TypeScript interfaces for ApiError, AuthState, LoadingState in frontend/types/index.ts
- [x] T007 Create centralized API client base with fetch wrapper in frontend/lib/api.ts
- [x] T008 Implement Authorization header injection in API client in frontend/lib/api.ts
- [x] T009 Implement 401 response detection and redirect logic in frontend/lib/api.ts
- [x] T010 Implement error response parsing in API client in frontend/lib/api.ts
- [x] T011 Add typed API methods (getTasks, createTask, updateTask, deleteTask, toggleComplete) in frontend/lib/api.ts
- [x] T012 [P] Create LoadingSpinner component with 44px touch target sizing in frontend/components/LoadingSpinner.tsx
- [x] T013 [P] Create ErrorMessage component with retry button in frontend/components/ErrorMessage.tsx
- [x] T014 Create root layout with basic HTML structure in frontend/app/layout.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin ✅

---

## Phase 3: User Story 6 - User Authentication Flow (Priority: P1) 🎯 MVP Foundation ✅ COMPLETE

**Goal**: Enable users to log in to access their tasks and log out when finished

**Independent Test**: Visit app unauthenticated (see login prompt), log in (access tasks), log out (return to login state)

### Implementation for User Story 6

- [x] T015 [US6] Create AuthContext with AuthProvider in frontend/lib/auth-context.tsx
- [x] T016 [US6] Implement in-memory token storage in AuthContext in frontend/lib/auth-context.tsx
- [x] T017 [US6] Implement login() and logout() methods in AuthContext in frontend/lib/auth-context.tsx
- [x] T018 [US6] Implement JWT token parsing to extract userId in frontend/lib/auth-context.tsx
- [x] T019 [US6] Wrap root layout with AuthProvider in frontend/app/layout.tsx
- [x] T020 [P] [US6] Create LoginForm component with email/password inputs in frontend/components/auth/LoginForm.tsx
- [x] T021 [US6] Add form validation and loading state to LoginForm in frontend/components/auth/LoginForm.tsx
- [x] T022 [US6] Add error display for failed login to LoginForm in frontend/components/auth/LoginForm.tsx
- [x] T023 [US6] Integrate LoginForm with Better Auth for token acquisition in frontend/components/auth/LoginForm.tsx
- [x] T024 [P] [US6] Create LogoutButton component in frontend/components/auth/LogoutButton.tsx
- [x] T025 [US6] Create login page with LoginForm in frontend/app/login/page.tsx
- [x] T026 [US6] Implement protected route logic - redirect unauthenticated to /login in frontend/app/layout.tsx
- [x] T027 [US6] Implement redirect authenticated users from /login to /tasks in frontend/app/login/page.tsx
- [x] T028 [US6] Connect API client 401 handling to auth context logout in frontend/lib/api.ts

**Checkpoint**: Authentication flow complete - users can log in and out ✅

---

## Phase 4: User Story 1 - View and Manage Task List (Priority: P1) 🎯 MVP Core ✅ COMPLETE

**Goal**: Authenticated users see a list of their personal tasks with title, completion status, and creation date

**Independent Test**: Authenticate user, navigate to main view, verify tasks displayed with correct completion status indicators

### Implementation for User Story 1

- [x] T029 [US1] Create TaskList component skeleton in frontend/components/TaskList.tsx
- [x] T030 [US1] Implement task fetching on mount using API client in frontend/components/TaskList.tsx
- [x] T031 [US1] Add loading state display during fetch in frontend/components/TaskList.tsx
- [x] T032 [US1] Add empty state message for no tasks in frontend/components/TaskList.tsx
- [x] T033 [US1] Add error state with retry button in frontend/components/TaskList.tsx
- [x] T034 [P] [US1] Create TaskItem component with title display in frontend/components/TaskItem.tsx
- [x] T035 [US1] Add completion status indicator (checkbox) to TaskItem in frontend/components/TaskItem.tsx
- [x] T036 [US1] Add title truncation with ellipsis for long titles in frontend/components/TaskItem.tsx
- [x] T037 [US1] Render TaskItem for each task in TaskList in frontend/components/TaskList.tsx
- [x] T038 [US1] Create tasks page composing TaskList in frontend/app/tasks/page.tsx
- [x] T039 [US1] Add responsive layout (mobile-first, desktop breakpoint 1024px) to tasks page in frontend/app/tasks/page.tsx
- [x] T040 [US1] Add LogoutButton to tasks page header in frontend/app/tasks/page.tsx
- [x] T041 [US1] Create landing page with auth-based redirect in frontend/app/page.tsx

**Checkpoint**: Users can view their task list with proper loading/empty/error states ✅

---

## Phase 5: User Story 2 - Create New Task (Priority: P1) 🎯 MVP Complete ✅ COMPLETE

**Goal**: Authenticated users can add new tasks to their list

**Independent Test**: Authenticate user, enter task title in form, submit, verify task appears in list

### Implementation for User Story 2

- [x] T042 [US2] Create AddTaskForm component with title input in frontend/components/AddTaskForm.tsx
- [x] T043 [US2] Add client-side validation (non-empty title) to AddTaskForm in frontend/components/AddTaskForm.tsx
- [x] T044 [US2] Add submit button with loading state to AddTaskForm in frontend/components/AddTaskForm.tsx
- [x] T045 [US2] Implement createTask API call on form submit in frontend/components/AddTaskForm.tsx
- [x] T046 [US2] Add error display for API failures in AddTaskForm in frontend/components/AddTaskForm.tsx
- [x] T047 [US2] Implement form reset on successful creation in frontend/components/AddTaskForm.tsx
- [x] T048 [US2] Add callback prop to notify TaskList of new task in frontend/components/AddTaskForm.tsx
- [x] T049 [US2] Integrate AddTaskForm into tasks page in frontend/app/tasks/page.tsx
- [x] T050 [US2] Implement task list refresh after successful creation in frontend/app/tasks/page.tsx

**Checkpoint**: Users can create tasks and see them in the list immediately ✅

---

## Phase 6: User Story 3 - Toggle Task Completion (Priority: P2) ✅ COMPLETE

**Goal**: Authenticated users can mark tasks as complete or incomplete

**Independent Test**: Authenticate user with tasks, click completion toggle, verify status changes and persists on refresh

### Implementation for User Story 3

- [x] T051 [US3] Add completion toggle click handler to TaskItem in frontend/components/TaskItem.tsx
- [x] T052 [US3] Add toggling loading state to TaskItem in frontend/components/TaskItem.tsx
- [x] T053 [US3] Implement toggleComplete API call in TaskItem in frontend/components/TaskItem.tsx
- [x] T054 [US3] Update task state on successful toggle in frontend/components/TaskItem.tsx
- [x] T055 [US3] Implement error handling - revert state and show error on failure in frontend/components/TaskItem.tsx
- [x] T056 [US3] Add visual feedback (checkbox state change) for completion in frontend/components/TaskItem.tsx
- [x] T057 [US3] Disable toggle interaction during API call in frontend/components/TaskItem.tsx

**Checkpoint**: Users can toggle task completion with visual feedback ✅

---

## Phase 7: User Story 4 - Update Existing Task (Priority: P2) ✅ COMPLETE

**Goal**: Authenticated users can edit task titles

**Independent Test**: Authenticate user, select task for editing, change title, save, verify updated title persists

### Implementation for User Story 4

- [x] T058 [US4] Add edit mode state to TaskItem in frontend/components/TaskItem.tsx
- [x] T059 [US4] Add edit button/trigger to TaskItem in frontend/components/TaskItem.tsx
- [x] T060 [US4] Create inline edit input field in TaskItem in frontend/components/TaskItem.tsx
- [x] T061 [US4] Add validation (non-empty title) for edit mode in frontend/components/TaskItem.tsx
- [x] T062 [US4] Add save and cancel buttons for edit mode in frontend/components/TaskItem.tsx
- [x] T063 [US4] Implement updateTask API call on save in frontend/components/TaskItem.tsx
- [x] T064 [US4] Add loading state during save in frontend/components/TaskItem.tsx
- [x] T065 [US4] Implement cancel to restore original value in frontend/components/TaskItem.tsx
- [x] T066 [US4] Implement error handling - show error and preserve original on failure in frontend/components/TaskItem.tsx

**Checkpoint**: Users can edit task titles inline with validation ✅

---

## Phase 8: User Story 5 - Delete Task (Priority: P3) ✅ COMPLETE

**Goal**: Authenticated users can remove tasks from their list

**Independent Test**: Authenticate user, select task for deletion, confirm action, verify task no longer appears

### Implementation for User Story 5

- [x] T067 [US5] Add delete button to TaskItem in frontend/components/TaskItem.tsx
- [x] T068 [US5] Implement confirmation dialog/prompt before deletion in frontend/components/TaskItem.tsx
- [x] T069 [US5] Add deleting loading state to TaskItem in frontend/components/TaskItem.tsx
- [x] T070 [US5] Implement deleteTask API call on confirm in frontend/components/TaskItem.tsx
- [x] T071 [US5] Add callback prop to notify TaskList of deleted task in frontend/components/TaskItem.tsx
- [x] T072 [US5] Remove task from list on successful deletion in frontend/components/TaskList.tsx
- [x] T073 [US5] Implement error handling - show error and keep task on failure in frontend/components/TaskItem.tsx
- [x] T074 [US5] Implement cancel to abort deletion in frontend/components/TaskItem.tsx

**Checkpoint**: Users can delete tasks with confirmation ✅

---

## Phase 9: Polish & Cross-Cutting Concerns ✅ COMPLETE

**Purpose**: Error handling improvements and responsive design finalization

- [x] T075 [P] Add network error detection and offline state display in frontend/lib/api.ts
- [x] T076 [P] Add backend unavailable (500/503) handling with retry in frontend/lib/api.ts
- [x] T077 Verify all error messages are user-friendly (no technical jargon) across all components
- [x] T078 [P] Finalize mobile layout (320px min) with proper spacing in frontend/app/tasks/page.tsx
- [x] T079 [P] Finalize desktop layout (1024px+) with optimized spacing in frontend/app/tasks/page.tsx
- [x] T080 Verify all touch targets are minimum 44x44 pixels across all components
- [x] T081 Run quickstart.md validation - verify development setup works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories ✅
- **User Story 6 (Phase 3)**: Depends on Foundational - Auth is prerequisite for all other stories ✅
- **User Stories 1-5 (Phase 4-8)**: All depend on User Story 6 (auth must work first) ✅
- **Polish (Phase 9)**: Depends on all user stories being complete ✅

### User Story Dependencies

```
Phase 1: Setup ✅
    ↓
Phase 2: Foundational (API Client, Types, Shared Components) ✅
    ↓
Phase 3: US6 - Authentication (BLOCKS all others) ✅
    ↓
┌───────────────────────────────────────┐
│  Phase 4: US1 - View Tasks (P1) ✅     │ ← MVP Core
│  Phase 5: US2 - Create Task (P1) ✅    │ ← MVP Complete
└───────────────────────────────────────┘
    ↓ (P1 stories complete)
┌───────────────────────────────────────┐
│  Phase 6: US3 - Toggle Complete (P2) ✅│
│  Phase 7: US4 - Update Task (P2) ✅    │
└───────────────────────────────────────┘
    ↓ (P2 stories complete)
Phase 8: US5 - Delete Task (P3) ✅
    ↓
Phase 9: Polish ✅
```

### Within Each User Story

- Core implementation before integration
- API calls before UI state management
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- US1 and US2 can run in parallel after US6 completes
- US3 and US4 can run in parallel after US1/US2 complete
- Different developers can work on different stories simultaneously

---

## Task Summary

| Phase | Story | Task Count | Completed |
|-------|-------|------------|-----------|
| 1 - Setup | - | 4 | 4 ✅ |
| 2 - Foundational | - | 10 | 10 ✅ |
| 3 - US6 Auth | P1 | 14 | 14 ✅ |
| 4 - US1 View | P1 | 13 | 13 ✅ |
| 5 - US2 Create | P1 | 9 | 9 ✅ |
| 6 - US3 Toggle | P2 | 7 | 7 ✅ |
| 7 - US4 Edit | P2 | 9 | 9 ✅ |
| 8 - US5 Delete | P3 | 8 | 8 ✅ |
| 9 - Polish | - | 7 | 7 ✅ |
| **Total** | | **81** | **81 ✅** |

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **IMPLEMENTATION COMPLETE**: All 81 tasks finished on 2026-02-06
