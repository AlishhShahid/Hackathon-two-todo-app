# Data Model: Todo In-Memory Python Console App

## Entity: Todo

### Fields
- **id** (int): Unique sequential identifier, assigned automatically, continues incrementing even after tasks are deleted
- **title** (str): Required task title, maximum 100 characters
- **description** (str): Optional task description, maximum 500 characters
- **completed** (bool): Task completion status, default False

### Validation Rules
- `id`: Must be unique, positive integer, auto-generated sequentially
- `title`: Required field, length between 1-100 characters, cannot be empty or whitespace-only
- `description`: Optional field, length between 0-500 characters
- `completed`: Boolean value only, default False when creating new tasks

### State Transitions
- **New Task**: `completed = False` (default)
- **Mark Complete**: `completed = True`
- **Mark Incomplete**: `completed = False`

## Entity: TodoRepository

### Fields
- **tasks** (dict): Dictionary storing Todo objects with ID as key
- **next_id** (int): Counter for the next available ID, starts at 1 and continues incrementing

### Validation Rules
- `tasks`: Must maintain unique IDs as keys
- `next_id`: Must always be greater than the highest existing ID in tasks

## Entity: TodoService

### Responsibilities
- Manage business logic for all Todo operations
- Coordinate between CLI layer and repository
- Handle validation and error cases

## Entity: TodoCLI

### Responsibilities
- Handle user input and command routing
- Format and display output to user
- Parse commands and call appropriate service methods