"""
Todo In-Memory Python Console App
In-memory repository for storing Todo objects
"""

from typing import Dict, List, Optional
from todo import Todo


class TodoRepository:
    """In-memory repository for storing Todo objects"""

    def __init__(self):
        """Initialize the repository with empty storage and ID counter"""
        self._tasks: Dict[int, Todo] = {}
        self._next_id = 1

    def add(self, todo: Todo) -> Todo:
        """
        Add a new Todo to the repository
        Assigns the next available ID to the todo
        """
        # If the todo doesn't have an ID yet, assign the next available one
        if todo.id == 0 or todo.id is None:
            todo.id = self._next_id
            self._next_id += 1
        elif todo.id >= self._next_id:
            # If a higher ID is provided, update the next_id counter
            self._next_id = todo.id + 1

        self._tasks[todo.id] = todo
        return todo

    def get(self, task_id: int) -> Optional[Todo]:
        """Retrieve a Todo by ID"""
        return self._tasks.get(task_id)

    def get_all(self) -> List[Todo]:
        """Retrieve all Todo objects"""
        return list(self._tasks.values())

    def update(self, task_id: int, updates: dict) -> Optional[Todo]:
        """Update properties of a Todo object"""
        todo = self.get(task_id)
        if todo:
            # Update the todo with the provided fields
            for field, value in updates.items():
                if hasattr(todo, field):
                    setattr(todo, field, value)
            # Re-validate after update
            todo._validate()
            return todo
        return None

    def delete(self, task_id: int) -> bool:
        """Delete a Todo by ID"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_next_id(self) -> int:
        """Get the next available ID for a new task"""
        return self._next_id

    def exists(self, task_id: int) -> bool:
        """Check if a task with the given ID exists"""
        return task_id in self._tasks