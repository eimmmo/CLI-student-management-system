import customtkinter as ctk

ctk.set_default_color_theme("blue")
from gui.frames import NavigationFrame, HomeFrame, TasksFrame, SettingsFrame
from t_manager import TaskManager
from settings_manager import SettingsManager
from notification_service import check_reminders
import threading
import time

class App(ctk.CTk):
    def __init__(self, task_manager, settings_manager):
        super().__init__()

        self.title("Task Manager")
        self.geometry("1368x720")

        self.task_manager = task_manager
        self.settings_manager = settings_manager

        # Configure the main window layout with a 1x2 grid (sidebar + content)
        # This ensures the content area expands to fill available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create the sidebar navigation frame
        # Using corner_radius=0 for a clean, modern look
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        # Make sure the navigation items are properly spaced
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Task Manager",
                                                     compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.tasks_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tasks",
                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              anchor="w", command=self.frame_2_button_event)
        self.tasks_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                              fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                              anchor="w", command=self.frame_3_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        # Initialize the main application frames
        # Each frame is created with a transparent background for a modern look
        self.home_frame = HomeFrame(self, fg_color="transparent")
        
        # The tasks frame includes the task management interface
        # We pass the task manager instance to handle all task-related operations
        self.tasks_frame = TasksFrame(self, task_manager=self.task_manager, fg_color="transparent")
        
        # Settings frame for user preferences
        # We pass the settings manager to handle user preferences
        self.settings_frame = SettingsFrame(self, settings_manager=self.settings_manager, fg_color="transparent")
        
        # Start with the home screen visible
        self.select_frame_by_name("home")

        # Start reminder check in a background thread
        self.reminder_thread = threading.Thread(target=self.run_reminder_check, daemon=True)
        self.reminder_thread.start()

    def select_frame_by_name(self, name):
        """
        Switch between different application views (home, tasks, settings)
        
        Args:
            name (str): Name of the frame to display ('home', 'tasks', or 'settings')
        """
        # Update button appearance to show which section is active
        # Active button gets a subtle background color
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.tasks_button.configure(fg_color=("gray75", "gray25") if name == "tasks" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # First, hide all frames to ensure a clean slate
        self.home_frame.grid_forget()
        self.tasks_frame.grid_forget()
        self.settings_frame.grid_forget()

        # Show the requested frame and perform any necessary updates
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "tasks":
            # Update the task list before showing the tasks frame
            self.tasks_frame.update_task_list()
            self.tasks_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            # Fallback: if an unknown frame is requested, show nothing
            self.settings_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("tasks")

    def frame_3_button_event(self):
        self.select_frame_by_name("settings")

    def run_reminder_check(self):
        """
        Background thread that periodically checks for due reminders
        Runs in a separate daemon thread to avoid blocking the main UI
        """
        while True:
            # Check for any tasks that need reminders
            check_reminders(self.task_manager, self.settings_manager)
            # Wait for an hour before checking again (3600 seconds)
            time.sleep(3600)

if __name__ == "__main__":
    # Initialize the application's data managers
    settings_manager = SettingsManager()
    task_manager = TaskManager()

    # Apply user preferences from settings on startup
    try:
        # Set the application's color theme (light/dark mode)
        appearance_mode = settings_manager.get_setting("appearance_mode")
        ctk.set_appearance_mode(appearance_mode)
        
        # Adjust UI scaling based on user preference
        ui_scaling = settings_manager.get_setting("ui_scaling").replace("%", "")
        scaling_float = int(ui_scaling) / 100
        ctk.set_widget_scaling(scaling_float)
    except (ValueError, AttributeError) as e:
        # If there's any issue with the saved settings, just use the defaults
        print(f"Using default settings due to: {e}")

    # Create and start the main application window
    app = App(task_manager=task_manager, settings_manager=settings_manager)
    app.mainloop()
