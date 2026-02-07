---
id: 1
title: Amend Constitution
stage: constitution
date: 2026-02-06
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 1-todo-app
user: user
command: /sp.constitution
labels: [constitution,spec-driven-development,todo-app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Project: Todo Full-Stack Web Application (Phase II of the Evolution of Todo).

Core principles:
- Spec-Driven Development (SDD): Strict adherence to the Specify → Plan → Tasks → Implement lifecycle. No agent is allowed to write code until the specification is complete and approved.
- The Golden Rule: No task = No code. Every implementation must map back to an explicit requirement and a unique Task ID.
- Stateless Architecture: The backend server and all future AI agents must remain stateless, persisting all session and task data to the database to ensure scalability and resilience.
- Architectural Hierarchy: The hierarchy of truth for this project is strictly defined as Constitution > Specify > Plan > Tasks.

Key standards:
- User Isolation: Every API request must be filtered by the authenticated user_id. Task ownership must be strictly enforced on every database operation.
- Secure Authentication: Implementation of Better Auth on the frontend and JWT (JSON Web Token) verification on the FastAPI backend using a shared BETTER_AUTH_SECRET.
- Clean Code & Structure: Proper Python project structure for the backend and Next.js App Router patterns for the frontend, following clean code principles.
- Centralised API Communication: All frontend-to-backend calls must go through a unified /lib/api.ts client to ensure consistent token handling.

Constraints:
- Technology Stack: Next.js 16+ (App Router), FastAPI, SQLModel (ORM), and Neon Serverless PostgreSQL.
- No Manual Coding: All implementation must be generated via Claude Code and Spec-Kit Plus based on refined specs. Writing code manually is strictly prohibited.
- Environment: Development must occur within a WSL 2 environment for Windows users.
- Monorepo Organization: Maintain a clear monorepo structure with /frontend, /backend, and a centralized /specs folder.

Success criteria:
- A fully functional web application implementing all 5 Basic Level features (Add, Delete, Update, View, Mark Complete).
- Successful authentication handshake where the backend correc

## Response snapshot

I have successfully updated the constitution file with the specific information for the Todo Full-Stack Web Application project. Here's a summary of what was done:

- Created a sync impact report showing the version change from 1.0.0 to 1.1.0
- Added 6 core principles as specified in the user input:
  1. Spec-Driven Development (SDD)
  2. The Golden Rule
  3. Stateless Architecture
  4. Architectural Hierarchy
  5. User Isolation
  6. Secure Authentication
- Added sections for Key Standards, Constraints, and Success Criteria
- Updated the version to 1.1.0 and set the last amended date to today (2026-02-06)
- Left the ratification date as a TODO since it wasn't provided

The constitution file at .specify/memory/constitution.md now contains all the specific project requirements and principles for the Todo Full-Stack Web Application project.

## Outcome

- ✅ Impact: Updated constitution with project-specific principles and constraints for Todo app
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new principles and project details
- 🔁 Next prompts: Continue with spec creation using /sp.specify
- 🧠 Reflection: Constitution successfully updated with all required project principles

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Proceed with specification creation