# Todo In-Memory Python Console App

A command-line todo application with in-memory storage that provides menu-driven single-letter commands for all basic todo operations.

## Features

- Add new tasks with title and description
- View all tasks with status indicators
- Mark tasks as complete/incomplete
- Update task details
- Delete tasks
- Menu-driven interface with single-letter commands

## Requirements

- Python 3.13 or higher

## Usage

1. Navigate to the project directory:
   ```bash
   cd todo-app
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Use the following single-letter commands:
   - `a` - Add a new task
   - `v` - View all tasks
   - `u` - Update a task
   - `d` - Delete a task
   - `c` - Mark task as complete
   - `i` - Mark task as incomplete
   - `q` - Quit the application

## Task Specifications

- **Title**: Required, 1-100 characters
- **Description**: Optional, 0-500 characters
- **Status**: Complete ([x]) or Incomplete ([ ])

## Architecture

The application follows a clean architecture pattern:

- **Presentation Layer** (`main.py`, `cli.py`): Handles user interaction and command routing
- **Service Layer** (`service.py`): Contains business logic and orchestrates operations
- **Data Layer** (`repository.py`): Manages in-memory storage of tasks
- **Domain Layer** (`todo.py`): Defines the Todo entity and its behavior

## Validation

- All inputs are validated according to specifications
- Clear error messages are provided for invalid inputs
- ID management continues incrementing even after task deletions