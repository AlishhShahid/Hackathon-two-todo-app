"""
Todo In-Memory Python Console App
CLI module for user interaction
"""

from service import TodoService
from repository import TodoRepository


class TodoCLI:
    """Command-line interface for the Todo application"""

    def __init__(self):
        """Initialize the CLI with service and repository"""
        self.repository = TodoRepository()
        self.service = TodoService(self.repository)
        self.running = True

    def display_menu(self):
        """Display the main menu with available commands"""
        print("\n" + "="*50)
        print("TODO APPLICATION")
        print("="*50)
        print("Available commands:")
        print("  a - Add a new task")
        print("  v - View all tasks")
        print("  u - Update a task")
        print("  d - Delete a task")
        print("  c - Mark task as complete")
        print("  i - Mark task as incomplete")
        print("  q - Quit the application")
        print("="*50)

    def get_user_input(self, prompt: str) -> str:
        """Get input from user with a prompt"""
        return input(prompt).strip()

    def run(self):
        """Main application loop"""
        print("Welcome to the Todo Console Application!")
        print("Type 'q' at any time to quit.")

        while self.running:
            self.display_menu()
            command = self.get_user_input("Enter command: ").lower()

            if command == 'q':
                self.quit()
            elif command == 'a':
                self.add_task()
            elif command == 'v':
                self.view_tasks()
            elif command == 'u':
                self.update_task()
            elif command == 'd':
                self.delete_task()
            elif command == 'c':
                self.mark_complete()
            elif command == 'i':
                self.mark_incomplete()
            else:
                print(f"Unknown command: '{command}'. Please try again.")

    def add_task(self):
        """Handle adding a new task"""
        print("\n--- Add New Task ---")
        title = self.get_user_input("Enter task title: ")

        if not title:
            print("Error: Title cannot be empty.")
            return

        description = self.get_user_input("Enter task description (optional, press Enter to skip): ")

        result = self.service.add_task(title, description)

        if result["success"]:
            task = result["task"]
            print(f"Task added successfully! ID: {task['id']}, Title: {task['title']}")
        else:
            print(f"Error: {result['error']}")

    def view_tasks(self):
        """Handle viewing all tasks"""
        print("\n--- View All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"Found {len(tasks)} task(s):")
        for task in tasks:
            status = "[x]" if task["completed"] else "[ ]"
            print(f"{status} {task['id']}. {task['title']}")
            if task["description"]:
                print(f"    Description: {task['description']}")

    def update_task(self):
        """Handle updating a task"""
        print("\n--- Update Task ---")

        try:
            task_id_str = self.get_user_input("Enter task ID to update: ")
            if not task_id_str:
                print("Task ID cannot be empty.")
                return
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        # Check if task exists first
        result = self.service.get_task(task_id)
        if not result["success"]:
            print(f"Error: {result['error']}")
            return

        current_task = result["task"]
        print(f"Current task: {current_task['title']}")
        if current_task["description"]:
            print(f"Current description: {current_task['description']}")

        new_title = self.get_user_input("Enter new title (or press Enter to keep current): ")
        new_description = self.get_user_input("Enter new description (or press Enter to keep current): ")

        # If user pressed Enter without typing, keep the current value
        if not new_title:
            new_title = None
        if not new_description:
            new_description = None

        result = self.service.update_task(task_id, new_title, new_description)

        if result["success"]:
            task = result["task"]
            print(f"Task updated successfully! ID: {task['id']}, Title: {task['title']}")
        else:
            print(f"Error: {result['error']}")

    def delete_task(self):
        """Handle deleting a task"""
        print("\n--- Delete Task ---")

        try:
            task_id_str = self.get_user_input("Enter task ID to delete: ")
            if not task_id_str:
                print("Task ID cannot be empty.")
                return
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        result = self.service.delete_task(task_id)

        if result["success"]:
            print(f"Task with ID {task_id} deleted successfully.")
        else:
            print(f"Error: {result['error']}")

    def mark_complete(self):
        """Handle marking a task as complete"""
        print("\n--- Mark Task Complete ---")

        try:
            task_id_str = self.get_user_input("Enter task ID to mark complete: ")
            if not task_id_str:
                print("Task ID cannot be empty.")
                return
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        result = self.service.mark_complete(task_id)

        if result["success"]:
            task = result["task"]
            print(f"Task '{task['title']}' marked as complete.")
        else:
            print(f"Error: {result['error']}")

    def mark_incomplete(self):
        """Handle marking a task as incomplete"""
        print("\n--- Mark Task Incomplete ---")

        try:
            task_id_str = self.get_user_input("Enter task ID to mark incomplete: ")
            if not task_id_str:
                print("Task ID cannot be empty.")
                return
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        result = self.service.mark_incomplete(task_id)

        if result["success"]:
            task = result["task"]
            print(f"Task '{task['title']}' marked as incomplete.")
        else:
            print(f"Error: {result['error']}")

    def quit(self):
        """Handle quitting the application"""
        print("Thank you for using the Todo Console Application!")
        self.running = False