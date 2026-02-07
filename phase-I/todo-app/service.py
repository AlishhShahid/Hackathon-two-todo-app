"""
Todo In-Memory Python Console App
TodoService with business logic
"""

from typing import Dict, List, Optional
from todo import Todo
from repository import TodoRepository


class TodoService:
    """Service layer for Todo operations with business logic"""

    def __init__(self, repository: TodoRepository):
        """
        Initialize the service with a repository

        Args:
            repository: TodoRepository instance to manage storage
        """
        self.repository = repository

    def add_task(self, title: str, description: str = "") -> Dict:
        """
        Add a new task to the repository with validation

        Args:
            title: Task title (1-100 characters)
            description: Task description (0-500 characters)

        Returns:
            Dict with success status and task data or error message
        """
        try:
            # Validate title length (1-100 characters)
            if not title or not title.strip():
                return {"success": False, "error": "Title cannot be empty or whitespace-only"}

            if len(title) < 1 or len(title) > 100:
                return {"success": False, "error": f"Title must be between 1 and 100 characters, got {len(title)}"}

            # Validate description length (0-500 characters)
            if len(description) > 500:
                return {"success": False, "error": f"Description must be 500 characters or less, got {len(description)}"}

            # Create and add the task
            next_id = self.repository.get_next_id()
            todo = Todo(id=next_id, title=title, description=description, completed=False)
            saved_todo = self.repository.add(todo)

            return {"success": True, "task": saved_todo.to_dict()}

        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get_all_tasks(self) -> List[Dict]:
        """Retrieve all tasks from the repository"""
        todos = self.repository.get_all()
        return [todo.to_dict() for todo in todos]

    def get_task(self, task_id: int) -> Dict:
        """
        Retrieve a specific task by ID

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Dict with success status and task data or error message
        """
        todo = self.repository.get(task_id)
        if todo:
            return {"success": True, "task": todo.to_dict()}
        else:
            return {"success": False, "error": f"Task with ID {task_id} does not exist"}

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict:
        """
        Update an existing task with validation

        Args:
            task_id: ID of the task to update
            title: New title (if provided, must be 1-100 characters)
            description: New description (if provided, must be 0-500 characters)

        Returns:
            Dict with success status and updated task data or error message
        """
        # Check if task exists
        if not self.repository.exists(task_id):
            return {"success": False, "error": f"Task with ID {task_id} does not exist"}

        # Validate title if provided
        if title is not None:
            if not title or not title.strip():
                return {"success": False, "error": "Title cannot be empty or whitespace-only"}

            if len(title) < 1 or len(title) > 100:
                return {"success": False, "error": f"Title must be between 1 and 100 characters, got {len(title)}"}

        # Validate description if provided
        if description is not None:
            if len(description) > 500:
                return {"success": False, "error": f"Description must be 500 characters or less, got {len(description)}"}

        # Prepare updates
        updates = {}
        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description

        # Perform update
        updated_todo = self.repository.update(task_id, updates)
        if updated_todo:
            return {"success": True, "task": updated_todo.to_dict()}
        else:
            return {"success": False, "error": "Failed to update task"}

    def delete_task(self, task_id: int) -> Dict:
        """
        Delete a task by ID

        Args:
            task_id: ID of the task to delete

        Returns:
            Dict with success status or error message
        """
        if not self.repository.exists(task_id):
            return {"success": False, "error": f"Task with ID {task_id} does not exist"}

        success = self.repository.delete(task_id)
        if success:
            return {"success": True}
        else:
            return {"success": False, "error": "Failed to delete task"}

    def mark_complete(self, task_id: int) -> Dict:
        """
        Mark a task as complete

        Args:
            task_id: ID of the task to mark complete

        Returns:
            Dict with success status and updated task data or error message
        """
        if not self.repository.exists(task_id):
            return {"success": False, "error": f"Task with ID {task_id} does not exist"}

        updated_todo = self.repository.update(task_id, {"completed": True})
        if updated_todo:
            return {"success": True, "task": updated_todo.to_dict()}
        else:
            return {"success": False, "error": "Failed to mark task as complete"}

    def mark_incomplete(self, task_id: int) -> Dict:
        """
        Mark a task as incomplete

        Args:
            task_id: ID of the task to mark incomplete

        Returns:
            Dict with success status and updated task data or error message
        """
        if not self.repository.exists(task_id):
            return {"success": False, "error": f"Task with ID {task_id} does not exist"}

        updated_todo = self.repository.update(task_id, {"completed": False})
        if updated_todo:
            return {"success": True, "task": updated_todo.to_dict()}
        else:
            return {"success": False, "error": "Failed to mark task as incomplete"}