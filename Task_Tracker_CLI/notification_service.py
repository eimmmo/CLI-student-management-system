"""
Notification Service for Task Manager

This module handles all notification-related functionality,
including checking for due tasks and displaying desktop notifications.
It uses the plyer library for cross-platform notification support.
"""

from datetime import datetime
from plyer import notification

def check_reminders(task_manager, settings_manager):
    """
    Check for tasks with reminders due today and send notifications.
    
    This function checks all tasks for any that have a reminder set for today.
    If notifications are enabled in settings, it will display a desktop notification
    for each due task.
    
    Args:
        task_manager: Instance of TaskManager containing the tasks to check
        settings_manager: Instance of SettingsManager to check notification preferences
    """
    # Skip if notifications are disabled in settings
    if not settings_manager.get_setting("notifications_enabled"):
        return

    # Get today's date and all tasks
    today = datetime.now().date()
    tasks = task_manager.get_all_tasks()

    # Check each task for reminders due today
    for task in tasks:
        if task.reminder and task.reminder == today:
            try:
                # Show a desktop notification for the due task
                notification.notify(
                    title='Task Reminder',
                    message=f'Task "{task.description}" is due today!',
                    app_name='Task Manager',
                    timeout=10  # Notification will auto-dismiss after 10 seconds
                )
            except Exception as e:
                # Log any errors that occur while sending notifications
                print(f"Error sending notification: {e}")
