# Research: Frontend UI & API Integration

**Feature Branch**: `003-frontend-todo-ui`
**Date**: 2026-02-06

## Research Areas

### 1. Next.js App Router Patterns

**Decision**: Use Next.js 16+ App Router with client-side rendering for the task management interface.

**Rationale**:
- App Router provides built-in support for layouts and nested routing
- Client components (with `"use client"` directive) are appropriate for interactive task management
- Server components not needed per spec (CSR acceptable, SSR out of scope)
- Better Auth integrates well with Next.js client-side patterns

**Alternatives Considered**:
- Pages Router: Legacy pattern, less optimal for new projects
- Full SSR: Out of scope per Non-Goals; adds complexity without benefit for this use case

### 2. JWT Token Storage Strategy

**Decision**: Store JWT tokens in-memory via React context/state management.

**Rationale**:
- Most secure option - tokens not accessible via XSS attacks through localStorage/sessionStorage
- Better Auth recommends session-based patterns compatible with in-memory storage
- Tradeoff (tokens lost on page refresh) acceptable for todo app - users re-authenticate
- Aligns with FR-017 requirement for secure storage

**Alternatives Considered**:
- localStorage: Vulnerable to XSS attacks
- sessionStorage: Better than localStorage but still XSS vulnerable
- httpOnly cookies: Requires backend coordination beyond scope

### 3. API Client Architecture

**Decision**: Singleton API client module at `/lib/api.ts` with typed methods for each endpoint.

**Rationale**:
- Centralizes authentication header attachment (FR-005)
- Single point for 401 handling and redirect logic (FR-006)
- Enforces no direct fetch calls (FR-007)
- Type-safe interfaces based on OpenAPI contract

**Alternatives Considered**:
- Axios instance: Additional dependency not needed; native fetch sufficient
- React Query/SWR: Could add later but unnecessary for MVP scope

### 4. State Management Approach

**Decision**: React Context for auth state; local component state for task data with prop drilling.

**Rationale**:
- Auth state (token, user info) is truly global - context appropriate
- Task state is page-scoped - simpler to manage locally
- Avoids premature optimization with external state libraries
- Matches simplicity principle (YAGNI)

**Alternatives Considered**:
- Redux/Zustand: Over-engineering for current scope
- React Query: Good for caching but adds complexity

### 5. Task Editing UX Pattern

**Decision**: Inline editing within TaskItem component.

**Rationale**:
- More direct user experience - click to edit without navigation
- Simpler implementation than modal overlay
- Matches common todo app patterns (Todoist, Google Tasks)
- Satisfies FR-013 requirement

**Alternatives Considered**:
- Modal editing: More steps for users; better for complex forms but overkill here
- Separate edit page: Poor UX for simple title changes

### 6. Responsive Design Approach

**Decision**: Mobile-first CSS with media queries for desktop breakpoints.

**Rationale**:
- Targets mobile (320px min) as base, enhances for desktop (1024px+) per FR-001
- No UI library per user requirements - vanilla CSS/Tailwind if available
- Touch targets 44x44px minimum for mobile usability (SC-006)

**Alternatives Considered**:
- Desktop-first: Harder to ensure mobile compatibility
- Component library (MUI, Chakra): Out of scope unless specified later

### 7. Error Handling Strategy

**Decision**: Error boundary at app level + inline error states per component.

**Rationale**:
- App-level boundary catches unexpected crashes
- Component-level error states for API failures (FR-003)
- User-friendly messages without technical jargon (SC-007)
- Retry capability for transient failures

**Alternatives Considered**:
- Global toast notifications only: Less contextual for users
- Full error page redirects: Disruptive for recoverable errors

### 8. Optimistic vs Pessimistic Updates

**Decision**: Pessimistic updates (wait for API confirmation before UI change) with loading states.

**Rationale**:
- Simpler to implement correctly
- Avoids complex rollback logic for failures
- Loading states provide user feedback (FR-002)
- Edge case spec says "UI reverts on error" which pessimistic handles naturally

**Alternatives Considered**:
- Optimistic updates: Better UX feel but requires rollback implementation; can add later

## Dependencies Confirmed

| Dependency | Status | Notes |
|------------|--------|-------|
| Spec 001 (Backend API) | Available | OpenAPI contract at `specs/001-todo-backend/contracts/openapi.yaml` |
| Spec 002 (Auth Security) | Available | JWT verification implemented in backend |
| Better Auth | Required | Must be configured for token issuance |
| Next.js 16+ | Required | Framework specified in user requirements |

## Open Questions Resolved

All NEEDS CLARIFICATION items from Technical Context have been resolved through this research.

## Next Steps

Proceed to Phase 1: Design & Contracts
- Generate `data-model.md` for frontend TypeScript interfaces
- Create `quickstart.md` for development setup
- Write implementation plan (`plan.md`)
