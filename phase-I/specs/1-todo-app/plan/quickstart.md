# Quickstart Guide: Todo In-Memory Python Console App

## Prerequisites

- Python 3.13 or higher
- UV package manager (for dependency management, though no external dependencies are required for this project)

## Setup Instructions

1. Clone the repository (if applicable) or create a new directory for the project
2. Create the project structure:
   ```
   todo-app/
   ├── main.py
   ├── todo.py
   ├── repository.py
   ├── service.py
   └── cli.py
   ```

## Project Structure

```
todo-app/
├── main.py          # Entry point with CLI loop
├── todo.py          # Todo data model
├── repository.py    # In-memory repository implementation
├── service.py       # TodoService with business logic
└── cli.py           # CLI interface and command routing
```

## Running the Application

1. Navigate to the project directory
2. Run the application:
   ```bash
   python main.py
   ```
3. The application will display a menu with single-letter commands:
   - `a` - Add a new task
   - `v` - View all tasks
   - `u` - Update a task
   - `d` - Delete a task
   - `c` - Mark task as complete
   - `i` - Mark task as incomplete
   - `q` - Quit the application

## Example Usage

1. Start the application: `python main.py`
2. Choose an option from the menu (e.g., press 'a' to add a task)
3. Follow the prompts to enter task details
4. The application will validate input according to the rules (100 char title limit, 500 char description limit)
5. Use 'v' to view your tasks with status indicators ([ ] for incomplete, [x] for complete)

## Development

The application is structured with clear separation of concerns:
- Data model (todo.py) handles the Todo entity
- Repository (repository.py) manages in-memory storage
- Service (service.py) contains business logic
- CLI (cli.py) handles user interaction
- Main (main.py) coordinates the application flow

This structure makes the application modular and easy to test or extend.