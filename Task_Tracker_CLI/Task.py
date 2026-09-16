from datetime import datetime

class Task:
    """
    Represents a single task in the Task Manager application.
    
    This class encapsulates all task-related data and behavior, including validation,
    serialization, and display formatting. It enforces business rules such as
    valid status values, priority levels, and reminder dates.
    """
    def __init__(self, id, description, status="todo", createdAt=None, updatedAt=None, reminder=None, priority="Medium", parent_id=None):
        """
        Initialize a new Task instance.
        
        Args:
            id (str): Unique identifier for the task
            description (str): Task description (at least 3 characters)
            status (str): Task status, one of: 'todo', 'in-progress', 'done'
            createdAt (str, optional): Creation timestamp. Auto-generated if not provided.
            updatedAt (str, optional): Last update timestamp. Auto-updated on changes.
            reminder (str/date, optional): Reminder date in YYYY-MM-DD format or date object
            priority (str): Task priority: 'Low', 'Medium', or 'High'
            parent_id (str, optional): ID of parent task for sub-tasks
        """
        # Convert string reminder to date object if needed
        if isinstance(reminder, str):
            reminder = datetime.strptime(reminder, '%Y-%m-%d').date()
            
        # Initialize task properties
        self.id = id
        self._description = description  # Using property setter for validation
        self._status = status            # Using property setter for validation
        self.createdAt = createdAt or self._get_current_time()
        self.updatedAt = updatedAt or self._get_current_time()
        self._reminder = reminder        # Using property setter for validation
        self._priority = priority        # Using property setter for validation
        self.parent_id = parent_id       # For sub-task relationships

    @property
    def description(self):
        """Get the task description."""
        return self._description

    @description.setter
    def description(self, value):
        """
        Set the task description.
        
        Args:
            value (str): New description (must be at least 3 characters)
            
        Raises:
            ValueError: If description is too short
        """
        if not value or len(value) < 3:
            raise ValueError("Description must be at least 3 characters long.")
        self._description = value
        self.touch()  # Update the 'updatedAt' timestamp

    @property
    def status(self):
        """Get the current status of the task."""
        return self._status

    @status.setter
    def status(self, value):
        """
        Update the task status.
        
        Args:
            value (str): New status, must be one of: 'todo', 'in-progress', 'done'
            
        Raises:
            ValueError: If status is not one of the allowed values
        """
        valid_statuses = ["todo", "in-progress", "done"]
        if value not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        self._status = value
        self.touch()  # Update the 'updatedAt' timestamp

    @property
    def reminder(self):
        """Get the reminder date as a date object, or None if not set."""
        return self._reminder

    @reminder.setter
    def reminder(self, value):
        """
        Set or update the reminder date.
        
        Args:
            value (str/date/None): Reminder date as string (YYYY-MM-DD) or date object
            
        Raises:
            ValueError: If date format is invalid or date is in the past
        """
        # Convert string to date object if needed
        if isinstance(value, str) and value:
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format for reminder. Use YYYY-MM-DD.")
                
        # Validate that reminder isn't in the past
        if value and value < datetime.now().date():
            raise ValueError("Reminder date cannot be in the past.")
            
        self._reminder = value
        self.touch()  # Update the 'updatedAt' timestamp

    @property
    def priority(self):
        """Get the task priority."""
        return self._priority

    @priority.setter
    def priority(self, value):
        """
        Set the task priority.
        
        Args:
            value (str): Priority level, must be 'Low', 'Medium', or 'High'
            
        Raises:
            ValueError: If priority is not one of the allowed values
        """
        valid_priorities = ["Low", "Medium", "High"]
        if value not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of: {', '.join(valid_priorities)}")
        self._priority = value
        self.touch()  # Update the 'updatedAt' timestamp

    def touch(self):
        """Update the 'updatedAt' timestamp to the current time."""
        self.updatedAt = self._get_current_time()

    def dict(self):
        """
        Convert the task to a dictionary for serialization.
        
        Returns:
            dict: A dictionary representation of the task suitable for JSON serialization
        """
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            'reminder': self.reminder.isoformat() if self.reminder else None,
            "priority": self.priority,
            "parent_id": self.parent_id
        }

    def display(self):
        """
        Get a formatted string representation of the task details.
        
        Returns:
            str: A multi-line string with all task information
        """
        info = (
            f"ID: {self.id}\n"
            f"Description: {self.description}\n"
            f"Status: {self.status}\n"
            f"Created At: {self.createdAt}\n"
            f"Updated At: {self.updatedAt}"
        )
        if self.reminder:
            info += f"\nReminder: {self.reminder}"
        info += f"\nPriority: {self.priority}"
        return info

    def _get_current_time(self):
        """
        Helper method to get the current timestamp.
        
        Returns:
            str: Current timestamp in 'YYYY-MM-DD HH:MM' format
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        """
        Get a brief string representation of the task.
        
        Returns:
            str: A short string with task ID, description, and status
        """
        return f"Task {self.id}: {self.description} ({self.status})"
