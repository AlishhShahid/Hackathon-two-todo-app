# Internal API Contracts: Todo In-Memory Python Console App

## TodoService Interface

### add_task(title: str, description: str = "") -> dict
- **Purpose**: Add a new task to the repository
- **Input**:
  - title (str, required): Task title (1-100 characters)
  - description (str, optional): Task description (0-500 characters)
- **Output**:
  - success (bool): True if task added successfully
  - task (dict): Task object if successful
  - error (str): Error message if failed
- **Validation**:
  - Title must be 1-100 characters
  - Description must be 0-500 characters
  - Title cannot be empty or whitespace-only

### get_all_tasks() -> list
- **Purpose**: Retrieve all tasks from repository
- **Input**: None
- **Output**: List of task dictionaries with id, title, description, completed

### get_task(task_id: int) -> dict
- **Purpose**: Retrieve a specific task by ID
- **Input**: task_id (int)
- **Output**:
  - success (bool): True if task exists
  - task (dict): Task object if found
  - error (str): Error message if not found

### update_task(task_id: int, title: str = None, description: str = None) -> dict
- **Purpose**: Update an existing task
- **Input**:
  - task_id (int): ID of task to update
  - title (str, optional): New title (1-100 characters if provided)
  - description (str, optional): New description (0-500 characters if provided)
- **Output**:
  - success (bool): True if update successful
  - task (dict): Updated task object if successful
  - error (str): Error message if failed

### delete_task(task_id: int) -> dict
- **Purpose**: Delete a task by ID
- **Input**: task_id (int)
- **Output**:
  - success (bool): True if deletion successful
  - error (str): Error message if failed

### mark_complete(task_id: int) -> dict
- **Purpose**: Mark a task as complete
- **Input**: task_id (int)
- **Output**:
  - success (bool): True if operation successful
  - task (dict): Updated task object if successful
  - error (str): Error message if failed

### mark_incomplete(task_id: int) -> dict
- **Purpose**: Mark a task as incomplete
- **Input**: task_id (int)
- **Output**:
  - success (bool): True if operation successful
  - task (dict): Updated task object if successful
  - error (str): Error message if failed

## TodoRepository Interface

### add(todo: Todo) -> Todo
- **Purpose**: Add a new Todo object to storage
- **Input**: Todo object with valid properties
- **Output**: The saved Todo object with assigned ID

### get(task_id: int) -> Todo
- **Purpose**: Retrieve a Todo object by ID
- **Input**: task_id (int)
- **Output**: Todo object if found, None otherwise

### get_all() -> list
- **Purpose**: Retrieve all Todo objects
- **Input**: None
- **Output**: List of all Todo objects

### update(task_id: int, updates: dict) -> Todo
- **Purpose**: Update properties of a Todo object
- **Input**: task_id (int), updates (dict of properties to update)
- **Output**: Updated Todo object if successful, None if not found

### delete(task_id: int) -> bool
- **Purpose**: Delete a Todo object by ID
- **Input**: task_id (int)
- **Output**: True if deletion successful, False if not found

### get_next_id() -> int
- **Purpose**: Get the next available ID for a new task
- **Input**: None
- **Output**: Next sequential ID that continues after deletions