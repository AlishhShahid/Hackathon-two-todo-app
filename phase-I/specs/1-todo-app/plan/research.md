# Research Document: Todo In-Memory Python Console App

## Architecture Analysis

Based on the user's architecture plan and feature specification, here are the key decisions and considerations:

### 1. Entry Point: main.py (CLI loop and command routing)

**Decision**: Implement a main.py file with a CLI loop that presents a menu-driven interface with single-letter commands as specified.

**Rationale**: This matches the specification requirement for menu-driven single-letter commands and provides a clear entry point for the application.

**Alternatives considered**:
- Command-line arguments instead of interactive menu (rejected - doesn't match spec requirement for menu-driven interface)
- Multiple entry points (rejected - overcomplicates single-user application)

### 2. Domain Model: Todo (id, title, completed)

**Decision**: Create a Todo class/data model with id, title, description, and completed status as specified in the feature requirements.

**Rationale**: The spec requires id (unique identifier), title (required), description (optional), and completion status (boolean). This matches the user's architecture plan with the addition of description as specified in the requirements.

**Alternatives considered**:
- Using a simple dictionary instead of a class (rejected - classes provide better structure and validation)
- Using Python dataclasses (selected approach - provides clean, structured data model)

### 3. In-memory Store: List-based repository

**Decision**: Implement an in-memory repository using Python lists/dictionaries to store Todo objects, with functionality to maintain unique sequential IDs as specified.

**Rationale**: The spec explicitly requires in-memory storage only, with unique sequential IDs that continue incrementing even after tasks are deleted.

**Alternatives considered**:
- Using a simple list (requires manual ID management)
- Using a dictionary with ID as key (selected approach - efficient lookups and maintains ID continuity)

### 4. Services: TodoService (business logic)

**Decision**: Create a TodoService class that encapsulates all business logic for task operations (add, view, update, delete, complete).

**Rationale**: Separation of concerns - keeps business logic separate from CLI interface and data models, making the code more maintainable and testable.

**Alternatives considered**:
- Direct operations in main.py (rejected - violates separation of concerns)
- Multiple service classes (rejected - over-engineering for simple application)

### 5. CLI Layer: Input parsing and output rendering

**Decision**: Implement a CLI layer that handles the menu-driven interface with single-letter commands as specified in the clarifications.

**Rationale**: Matches the specification requirement for menu-driven single-letter commands (e.g., 'a' to add, 'v' to view, 'd' to delete).

**Alternatives considered**:
- Full command names (rejected - doesn't match specification)
- Number-based menu options (rejected - single letters are more efficient)

### 6. Validation and Error Handling

**Decision**: Implement validation for character limits (100 for title, 500 for description) and proper error handling for invalid inputs as specified in the requirements.

**Rationale**: The spec explicitly requires these validation rules and error handling.

**Alternatives considered**: No validation (rejected - violates specification)

## Technology Stack

**Python 3.13+**: As specified in the user's architecture plan
**No external dependencies**: As specified in the constraints (pure Python)
**UV package manager**: As specified in the constraints

## Implementation Approach

Based on the user's implementation steps and the feature specification, the approach will be:

1. Define Todo data model with proper validation
2. Implement in-memory repository with ID management
3. Implement TodoService with all required operations
4. Build CLI command interface with menu-driven flow
5. Add input validation and user feedback
6. Final manual test via console

## Risk Assessment

**Low Risk Items**:
- In-memory storage (simple to implement)
- Single-user application (no concurrency concerns)
- Well-defined requirements (clear acceptance criteria)

**Potential Challenges**:
- Maintaining unique sequential IDs that don't reset after deletion
- Proper validation of character limits
- Clear error messaging as specified in requirements