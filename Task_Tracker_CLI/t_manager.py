import json
import csv
from datetime import datetime
from Task import Task
from error_handler import TaskError

class TaskManager:
    """
    Manages all task-related operations including CRUD operations and file persistence.
    
    This class handles the core functionality of the task management system,
    including loading/saving tasks to a JSON file and maintaining task state.
    """
    def __init__(self, filename='tasks.json'):
        """
        Initialize the TaskManager with a JSON file for storage.
        
        Args:
            filename (str): Path to the JSON file for storing tasks.
        """
        self.filename = filename  # File where tasks are stored
        self._tasks = {}          # Dictionary to hold tasks with IDs as keys
        self._next_id = 1         # Counter for generating unique task IDs
        self.load_tasks()         # Load existing tasks from file

    def load_tasks(self):
        """
        Load tasks from the JSON file into memory.
        
        This method reads the tasks from the JSON file and populates the _tasks dictionary.
        If the file doesn't exist, it starts with an empty task list.
        """
        try:
            with open(self.filename, 'r') as file:
                # Load all tasks from the JSON file
                tasks_data = json.load(file)
                
                # Process each task in the file
                for task_item in tasks_data:
                    # Get the task ID, skip if missing (invalid task)
                    task_id = task_item.get('id')
                    if task_id is None:
                        continue
                        
                    # Remove the ID from the task data to avoid passing it twice to Task constructor
                    task_item.pop('id', None)
                    
                    # Create a new Task object and add it to our tasks dictionary
                    self._tasks[str(task_id)] = Task(id=str(task_id), **task_item)

                # Update the next available ID to be one more than the highest existing ID
                if self._tasks:
                    self._next_id = max(int(k) for k in self._tasks.keys()) + 1
                    
        # Handle various error cases
        except FileNotFoundError:
            # File doesn't exist yet - start with empty task list
            self._tasks = {}
        except (json.JSONDecodeError, IOError, OSError, ValueError) as e:
            # Handle file corruption or permission issues
            raise TaskError(f"Error loading tasks file: {e}")

    def save_tasks(self):
        """
        Save all tasks to the JSON file.
        
        This method writes the current state of all tasks to the JSON file.
        The file is created if it doesn't exist, and existing content is overwritten.
        """
        try:
            # Convert all tasks to dictionaries and save to file with nice formatting
            with open(self.filename, 'w') as file:
                # Create a list of task dictionaries and save with pretty-printing
                tasks_data = [task.dict() for task in self._tasks.values()]
                json.dump(tasks_data, file, indent=4)
                
        except (IOError, OSError) as e:
            # Handle file writing errors (e.g., disk full, permission issues)
            raise TaskError(f"Could not save tasks to {self.filename}: {e}")

    def add_task(self, description, reminder=None, priority='Medium', parent_id=None):
        """
        Add a new task to the task manager.
        
        Args:
            description (str): The task description (required)
            reminder (str, optional): Reminder time in ISO format
            priority (str): Priority level ('Low', 'Medium', or 'High')
            parent_id (str, optional): ID of the parent task for sub-tasks
            
        Returns:
            Task: The newly created task
            
        Raises:
            TaskError: If there's an error creating or saving the task
        """
        # Generate a new unique ID for this task
        task_id = str(self._next_id)
        
        try:
            # Create a new Task object with the provided details
            task = Task(
                id=task_id,
                description=description,
                reminder=reminder,
                priority=priority,
                parent_id=parent_id
            )
            
            # Add the task to our dictionary and update the next available ID
            self._tasks[task_id] = task
            self._next_id += 1
            
            # Save all tasks to persist the new task
            self.save_tasks()
            return task
            
        except ValueError as e:
            # Handle validation errors from the Task class
            raise TaskError(str(e))

    def get_all_tasks(self, sort_by=None, search_query=None):
        """
        Retrieve all tasks, optionally filtered and sorted.
        
        Args:
            sort_by (str, optional): Field to sort by. Currently supports 'priority'.
            search_query (str, optional): Filter tasks by matching this string in the description.
            
        Returns:
            list: A list of Task objects matching the criteria.
        """
        # Start with a copy of all tasks
        tasks = list(self._tasks.values())

        # Apply search filter if provided (case-insensitive search in description)
        if search_query:
            search_lower = search_query.lower()
            tasks = [task for task in tasks if search_lower in task.description.lower()]
            
        # Apply sorting if requested
        if sort_by == 'priority':
            # Map priority levels to sort order (High=0, Medium=1, Low=2, others=99)
            priority_map = {'High': 0, 'Medium': 1, 'Low': 2}
            tasks.sort(key=lambda t: priority_map.get(t.priority, 99))
            
        return tasks

    def list_by_status(self, status):
        """
        Get all tasks with a specific status.
        
        Args:
            status (str): The status to filter by (e.g., 'todo', 'in-progress', 'done')
            
        Returns:
            list: Tasks that match the specified status
        """
        return [task for task in self._tasks.values() if task.status == status]

    def find_task_by_id(self, task_id):
        """
        Find a task by its ID.
        
        Args:
            task_id (str): The ID of the task to find
            
        Returns:
            Task: The found task
            
        Raises:
            TaskError: If no task exists with the given ID
        """
        task = self._tasks.get(str(task_id))
        if not task:
            raise TaskError(f"Task with ID {task_id} not found.")
        return task

    def export_tasks(self, file_path, file_format):
        """
        Export tasks to a file in the specified format.
        
        Args:
            file_path (str): Path where the exported file should be saved
            file_format (str): Format to export to (currently only 'CSV' is supported)
            
        Raises:
            ValueError: If an unsupported format is requested
        """
        if file_format == "CSV":
            self._export_to_csv(file_path)
        else:
            raise ValueError(f"Unsupported export format: {file_format}")

    def _export_to_csv(self, file_path):
        """
        Internal method to export tasks to a CSV file.
        
        Args:
            file_path (str): Path where the CSV file should be saved
        """
        tasks = self.get_all_tasks()
        if not tasks:
            return  # No tasks to export

        # Define the CSV structure with all possible task fields
        fieldnames = [
            'id', 'description', 'status', 'createdAt', 
            'updatedAt', 'reminder', 'priority', 'parent_id'
        ]
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                # Create a CSV writer with our field names
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()  # Write the header row
                
                # Write each task as a row in the CSV
                for task in tasks:
                    # Get task data as a dictionary and ensure all fields are present
                    task_dict = task.dict()
                    row = {field: task_dict.get(field) for field in fieldnames}
                    writer.writerow(row)
                    
        except (IOError, OSError) as e:
            raise TaskError(f"Failed to write to CSV file: {e}")


    def edit_task(self, task_id, new_description=None, new_status=None, new_reminder=None, new_priority=None, new_parent_id=None):
        """
        Update an existing task with new values.
        
        Only the specified fields will be updated. All parameters except task_id are optional.
        
        Args:
            task_id (str): ID of the task to update
            new_description (str, optional): New task description
            new_status (str, optional): New status ('todo', 'in-progress', 'done')
            new_reminder (str, optional): New reminder time in ISO format
            new_priority (str, optional): New priority level ('Low', 'Medium', 'High')
            new_parent_id (str, optional): New parent task ID for sub-tasks
            
        Returns:
            Task: The updated task
            
        Raises:
            TaskError: If the task doesn't exist or there's a validation error
        """
        # Find the task first (this will raise TaskError if not found)
        task = self.find_task_by_id(str(task_id))
        
        try:
            # Only update the fields that were provided
            if new_description is not None:
                task.description = new_description
            if new_status is not None:
                task.status = new_status
            if new_reminder is not None:
                task.reminder = new_reminder
            if new_priority is not None:  # Changed from 'if new_priority' to handle empty string
                task.priority = new_priority
            if new_parent_id is not None:
                task.parent_id = new_parent_id
                
            # Save changes to disk
            self.save_tasks()
            return task
            
        except ValueError as e:
            # Re-raise validation errors as TaskError
            raise TaskError(str(e))

    def delete_task(self, task_id):
        """
        Delete a task by its ID.
        
        Args:
            task_id (str): The ID of the task to delete
            
        Raises:
            TaskError: If the task doesn't exist
        """
        # First verify the task exists (raises TaskError if not found)
        task_id = str(task_id)
        self.find_task_by_id(task_id)
        
        # Remove the task and save changes
        del self._tasks[task_id]
        self.save_tasks()

