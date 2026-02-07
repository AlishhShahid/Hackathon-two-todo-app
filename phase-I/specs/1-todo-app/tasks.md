# Implementation Tasks: Todo In-Memory Python Console App

## Feature Overview

**Feature**: Todo In-Memory Python Console App
**Branch**: 1-todo-app
**Created**: 2026-01-02
**Status**: Task Breakdown

This document breaks down the implementation of a command-line todo application with in-memory storage. The app provides menu-driven single-letter commands for all basic todo operations.

## Implementation Strategy

- **MVP First**: Implement User Story 1 (Add Tasks) as the minimum viable product
- **Incremental Delivery**: Each user story builds on the previous one
- **Independent Testing**: Each user story can be tested independently
- **Clean Architecture**: Follow layered architecture with separation of concerns

## Dependencies

- User Story 1 (Add Tasks) must be completed before User Story 2 (View Tasks)
- User Story 2 (View Tasks) enables User Story 3 (Mark Complete/Incomplete)
- User Stories 4 and 5 depend on the foundational components established in Stories 1-3

## Parallel Execution Examples

- **Story 1**: [P] Implement Todo model and [P] Implement Repository can run in parallel
- **Story 2**: [P] CLI display and [P] Service methods can run in parallel
- **Stories 3-5**: Each can be developed in parallel once foundational components are complete

---

## Phase 1: Setup

**Goal**: Initialize project structure and foundational components

**Independent Test**: Project structure allows for clean imports and module organization

- [X] T001 Create project directory structure (todo-app/main.py, todo-app/todo.py, todo-app/repository.py, todo-app/service.py, todo-app/cli.py)
- [X] T002 Set up Python virtual environment with Python 3.13+ requirements
- [X] T003 Create requirements.txt file (empty initially, as no external dependencies are required)

---

## Phase 2: Foundational Components

**Goal**: Implement core data model and repository with proper ID management

**Independent Test**: Can create Todo objects and store/retrieve them in memory with unique sequential IDs

- [X] T004 [P] Create Todo data model in todo.py with id, title, description, completed fields and validation
- [X] T005 [P] Create TodoRepository in repository.py with in-memory storage and ID management
- [X] T006 Implement validation for title (1-100 chars) and description (0-500 chars) in Todo model
- [X] T007 Test ID management that continues incrementing after deletions in repository

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1)

**Goal**: Users can add new tasks with title and description to the in-memory store

**Independent Test**: Can run the add command with a title and description, then verify the task appears in the list

- [X] T008 [P] [US1] Create add_task method in TodoService with validation for title and description
- [X] T009 [P] [US1] Implement add command in CLI module to handle user input
- [X] T010 [US1] Implement main application loop to route to add functionality
- [X] T011 [US1] Test acceptance scenario: add command with valid title and description creates task with unique ID
- [X] T012 [US1] Test acceptance scenario: add command with missing title shows error message
- [X] T013 [US1] Test acceptance scenario: title longer than 100 characters shows error
- [X] T014 [US1] Test acceptance scenario: description longer than 500 characters shows error

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Users can see all their tasks in a formatted list with status indicators

**Independent Test**: Can add tasks then use the view command to display them with proper status indicators

- [X] T015 [P] [US2] Create get_all_tasks method in TodoService
- [X] T016 [P] [US2] Implement view command in CLI module to display tasks with [ ]/[x] indicators
- [X] T017 [US2] Format task display with ID, title, description, and completion status
- [X] T018 [US2] Test acceptance scenario: multiple tasks display with proper status indicators
- [X] T019 [US2] Test acceptance scenario: no tasks message displays when list is empty

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P1)

**Goal**: Users can mark tasks as complete when finished or incomplete if revisiting

**Independent Test**: Can add tasks, toggle their status, and verify status changes when viewing the list

- [X] T020 [P] [US3] Create mark_complete and mark_incomplete methods in TodoService
- [X] T021 [P] [US3] Implement complete and incomplete commands in CLI module
- [X] T022 [US3] Add validation to ensure task exists before changing status
- [X] T023 [US3] Test acceptance scenario: valid task ID changes to complete status
- [X] T024 [US3] Test acceptance scenario: valid task ID changes to incomplete status
- [X] T025 [US3] Test acceptance scenario: invalid task ID shows appropriate error message

---

## Phase 6: User Story 4 - Update Task Details (Priority: P2)

**Goal**: Users can modify the details of an existing task

**Independent Test**: Can add a task, update its details, and verify changes reflect when viewing the list

- [X] T026 [P] [US4] Create update_task method in TodoService with validation
- [X] T027 [P] [US4] Implement update command in CLI module to handle user input
- [X] T028 [US4] Add validation for updated title (1-100 chars) and description (0-500 chars)
- [X] T029 [US4] Test acceptance scenario: valid task ID and new details update successfully
- [X] T030 [US4] Test acceptance scenario: invalid task ID shows appropriate error message

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Users can remove tasks from their todo list

**Independent Test**: Can add tasks, delete one, and verify it no longer appears in the task list

- [X] T031 [P] [US5] Create delete_task method in TodoService that maintains ID continuity
- [X] T032 [P] [US5] Implement delete command in CLI module
- [X] T033 [US5] Ensure ID counter continues incrementing after deletion
- [X] T034 [US5] Test acceptance scenario: valid task ID removes task from system
- [X] T035 [US5] Test acceptance scenario: invalid task ID shows appropriate error message

---

## Phase 8: CLI Integration & Menu System

**Goal**: Implement the complete menu-driven interface with single-letter commands

**Independent Test**: All commands work through the menu-driven interface with proper single-letter shortcuts

- [X] T036 [P] Implement main menu display with all available commands
- [X] T037 [P] Map single-letter commands: 'a' (add), 'v' (view), 'u' (update), 'd' (delete), 'c' (complete), 'i' (incomplete), 'q' (quit)
- [X] T038 Create command routing system in main.py
- [X] T039 Implement graceful exit functionality
- [X] T040 Test complete menu flow with all commands

---

## Phase 9: Error Handling & Validation

**Goal**: Ensure all edge cases and error conditions are handled properly

**Independent Test**: All error scenarios from the specification are handled with clear messages

- [X] T041 [P] Implement consistent error message format across all operations
- [X] T042 [P] Add validation for all user inputs throughout the application
- [X] T043 Handle non-existent task ID access with appropriate error messages
- [X] T044 Handle empty input for titles and descriptions
- [X] T045 Validate character limits are enforced throughout the application

---

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Final integration, testing, and refinement

**Independent Test**: Complete application functions as specified with all features working together

- [X] T046 [P] Implement comprehensive error handling throughout the application
- [X] T047 [P] Add clear prompts and user feedback for all operations
- [X] T048 Conduct end-to-end testing of all user stories together
- [X] T049 Verify all functional requirements (FR-001 through FR-010) are met
- [X] T050 Verify all success criteria (SC-001 through SC-005) are met
- [X] T051 Final code review and refactoring for readability
- [X] T052 Update README with usage instructions