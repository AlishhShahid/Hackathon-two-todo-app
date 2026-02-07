"""
Todo In-Memory Python Console App
Todo data model with validation
"""

import re
from typing import Optional


class Todo:
    """Represents a single todo item with ID, title, description, and completion status"""

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a Todo object

        Args:
            id: Unique sequential identifier
            title: Required task title (1-100 characters)
            description: Optional task description (0-500 characters)
            completed: Task completion status (default False)
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self._validate()

    def _validate(self):
        """Validate the Todo object's fields"""
        # Validate title (required, 1-100 characters)
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        if len(self.title) < 1 or len(self.title) > 100:
            raise ValueError(f"Title must be between 1 and 100 characters, got {len(self.title)}")

        # Validate description (optional, 0-500 characters)
        if len(self.description) > 500:
            raise ValueError(f"Description must be 500 characters or less, got {len(self.description)}")

    def update(self, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None):
        """Update todo fields with validation"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if completed is not None:
            self.completed = completed
        self._validate()

    def __str__(self):
        """String representation of the Todo"""
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}. {self.title}"

    def to_dict(self):
        """Convert Todo to dictionary representation"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    def to_detailed_str(self):
        """Detailed string representation for viewing tasks"""
        status = "[x]" if self.completed else "[ ]"
        result = f"{status} {self.id}. {self.title}\n"
        if self.description:
            result += f"    Description: {self.description}\n"
        return result