import customtkinter as ctk
from tkcalendar import DateEntry
from .dialogs import TaskDialog, ConfirmationDialog, ErrorDialog, ExportDialog

# This frame can be used to hold navigation controls
class NavigationFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

# This is the main welcome screen that displays app info and features
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # Welcome message
        welcome_frame = ctk.CTkFrame(self, fg_color="transparent")
        welcome_frame.pack(pady=40, padx=20, fill="x")
        
        self.label = ctk.CTkLabel(welcome_frame, 
                                text="Welcome to the Task Manager!", 
                                font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(0, 10))
        
        # Description
        description = ("A modern task management application with a clean interface, "
                     "task prioritization, due dates, and more.")
        self.desc_label = ctk.CTkLabel(welcome_frame, 
                                     text=description,
                                     wraplength=600,
                                     justify="center",
                                     text_color=("gray50", "gray70"),
                                     font=ctk.CTkFont(size=14))
        self.desc_label.pack(pady=(0, 40))
        
        # Features grid
        features_frame = ctk.CTkFrame(self, fg_color="transparent")
        features_frame.pack(fill="x", padx=40, pady=20)
        
        features = [
            "✓ Task management with status tracking",
            "✓ Priority levels for better organization",
            "✓ Due dates and reminders",
            "✓ Hierarchical sub-tasks",
            "✓ Search and filter capabilities",
            "✓ Export tasks to CSV"
        ]
        
        for i, feature in enumerate(features):
            label = ctk.CTkLabel(features_frame, 
                               text=feature,
                               font=ctk.CTkFont(size=14),
                               anchor="w")
            label.grid(row=i//2, column=i%2, sticky="w", padx=20, pady=5)
        
        # Credits section
        credits_frame = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        credits_frame.pack(side="bottom", fill="x", padx=20, pady=20, ipady=10)
        
        credits_title = ctk.CTkLabel(credits_frame, 
                                   text="Credits",
                                   font=ctk.CTkFont(size=16, weight="bold"))
        credits_title.pack(pady=(5, 10))
        
        credits_text = ("Task Manager v1.0\n"
                      "Developed with Python and CustomTkinter\n"
                      "Made with Love By Eman Abd EL-Rahman")
        
        credits_label = ctk.CTkLabel(credits_frame,
                                   text=credits_text,
                                   justify="center",
                                   text_color=("gray40", "gray60"),
                                   font=ctk.CTkFont(size=12))
        credits_label.pack(pady=(0, 5))

# Settings page where user can customize appearance, scaling, and notifications
class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, settings_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.settings_manager = settings_manager

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Appearance Mode
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        current_mode = self.settings_manager.get_setting("appearance_mode")
        self.appearance_mode_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_menu.set(current_mode)
        self.appearance_mode_menu.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="w")

        # UI Scaling
        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")

        current_scaling = self.settings_manager.get_setting("ui_scaling")
        self.scaling_optionemenu = ctk.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                       command=self.change_scaling_event)
        self.scaling_optionemenu.set(current_scaling)
        self.scaling_optionemenu.grid(row=2, column=1, padx=20, pady=(10, 0), sticky="w")

        # Notifications
        self.notifications_label = ctk.CTkLabel(self, text="Enable Notifications:", anchor="w")
        self.notifications_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.notifications_switch = ctk.CTkSwitch(self, text="", command=self.toggle_notifications)
        self.notifications_switch.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="w")

        # Set initial switch state
        if self.settings_manager.get_setting("notifications_enabled"):
            self.notifications_switch.select()
    
    # Change app appearance when dropdown changes
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.settings_manager.set_setting("appearance_mode", new_appearance_mode)

    # Change UI scaling percentage
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        self.settings_manager.set_setting("ui_scaling", new_scaling)

    # Enable or disable notifications
    def toggle_notifications(self):
        is_enabled = self.notifications_switch.get() == 1
        self.settings_manager.set_setting("notifications_enabled", is_enabled)


# Status control for changing task status
class StatusControl(ctk.CTkFrame):
    def __init__(self, master, task, task_manager, on_update):
        super().__init__(master, fg_color="transparent")
        self.task = task
        self.task_manager = task_manager
        self.on_update = on_update

        self.status_var = ctk.StringVar(value=self.task.status)

        self.todo_rb = ctk.CTkRadioButton(self, text="To Do", variable=self.status_var, value="todo", command=self.update_status)
        self.inprogress_rb = ctk.CTkRadioButton(self, text="In Progress", variable=self.status_var, value="in-progress", command=self.update_status)
        self.done_rb = ctk.CTkRadioButton(self, text="Done", variable=self.status_var, value="done", command=self.update_status)

        self.todo_rb.grid(row=0, column=0, padx=5, pady=2)
        self.inprogress_rb.grid(row=0, column=1, padx=5, pady=2)
        self.done_rb.grid(row=0, column=2, padx=5, pady=2)

    # Set the initial state based on the task's status
    def update_status(self):
        new_status = self.status_var.get()
        try:
            self.task_manager.edit_task(self.task.id, new_status=new_status)
            self.on_update()
        except Exception as e:
            ErrorDialog(self, "Error", f"Failed to update status: {e}")

# Main frame that displays tasks and allows management
class TasksFrame(ctk.CTkFrame):
    def __init__(self, master, task_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.task_manager = task_manager
        self.selected_task_id = None
        self.current_filter = "All"
        self.sort_by_priority_enabled = False
        self._search_query = ""
        self._start_date = None
        self._end_date = None
        self.configure(fg_color="transparent")

        # Add a grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Controls frame
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.add_button = ctk.CTkButton(self.controls_frame, text="Add Task", command=self.add_task_event)
        self.add_button.pack(side="left")

        self.edit_button = ctk.CTkButton(self.controls_frame, text="Edit Task", command=self.edit_task_event)
        self.edit_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(self.controls_frame, text="Delete Task", command=self.delete_task_event)
        self.delete_button.pack(side="left")

        self.add_subtask_button = ctk.CTkButton(self.controls_frame, text="Add Sub-Task", command=self.add_subtask_event, state="disabled")
        self.add_subtask_button.pack(side="left", padx=10)

        self.export_button = ctk.CTkButton(self.controls_frame, text="Export Tasks", command=self.export_tasks_event)
        self.export_button.pack(side="left", padx=10)

        # Search and filter controls
        filter_controls_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        filter_controls_frame.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.search_entry = ctk.CTkEntry(filter_controls_frame, placeholder_text="Search...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self._on_search())

        self.sort_button = ctk.CTkButton(filter_controls_frame, text="Sort by Priority", command=self.toggle_sort_by_priority)
        self.sort_button.pack(side="left", padx=(0, 10))

        self.filter_button = ctk.CTkSegmentedButton(filter_controls_frame, values=["All", "todo", "in-progress", "done"], command=self.filter_tasks)
        self.filter_button.set("All")
        self.filter_button.pack(side="left")

        # Date range filter
        self.start_date_label = ctk.CTkLabel(filter_controls_frame, text="From:")
        self.start_date_label.pack(side="left", padx=(10, 0))
        self.start_date_entry = DateEntry(filter_controls_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.start_date_entry.pack(side="left")
        self.start_date_entry.delete(0, "end")

        self.end_date_label = ctk.CTkLabel(filter_controls_frame, text="To:")
        self.end_date_label.pack(side="left", padx=(5, 0))
        self.end_date_entry = DateEntry(filter_controls_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.end_date_entry.pack(side="left")
        self.end_date_entry.delete(0, "end")

        self.date_filter_button = ctk.CTkButton(filter_controls_frame, text="Filter Date", width=80, command=self._apply_date_filter)
        self.date_filter_button.pack(side="left", padx=5)

        # Scrollable frame for tasks
        self.task_list_frame = ctk.CTkScrollableFrame(self)
        self.task_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.update_task_list()

    # Open dialog to add new task
    def add_task_event(self):
        dialog = TaskDialog(self, "Add Task", self.task_manager)
        self.wait_window(dialog)

    # Open dialog to add a sub-task to the selected task
    def add_subtask_event(self):
        if self.selected_task_id is None:
            ErrorDialog(self, "Error", "Please select a parent task first.")
            return
        dialog = TaskDialog(self, "Add Sub-Task", self.task_manager, parent_id=self.selected_task_id)
        self.wait_window(dialog)

    # Open dialog to edit the selected task
    def edit_task_event(self):
        if self.selected_task_id is None:
            ErrorDialog(self, "Error", "Please select a task to edit.")
            return
        try:
            task = self.task_manager.find_task_by_id(self.selected_task_id)
            dialog = TaskDialog(self, "Edit Task", self.task_manager, task=task)
            self.wait_window(dialog)
        except Exception as e:
            ErrorDialog(self, "Error", str(e))

    # Handle deleting tasks and subtasks with confirmation
    def delete_task_event(self):
        if self.selected_task_id is None:
            ErrorDialog(self, "Error", "Please select a task to delete.")
            return

        children = [task for task in self.task_manager.get_all_tasks() if task.parent_id == self.selected_task_id]

        if children:
            dialog = ConfirmationDialog(self, "Delete Parent Task", "This task has sub-tasks. Delete them as well?")
            self.wait_window(dialog)
            if dialog.result:
                # Delete parent and all children
                self._delete_task_recursively(self.selected_task_id)
            else:
                # Make children top-level tasks
                for child in children:
                    self.task_manager.edit_task(child.id, new_parent_id=None)
                self.task_manager.delete_task(self.selected_task_id)
        else:
            dialog = ConfirmationDialog(self, "Confirm Deletion", "Are you sure you want to delete this task?")
            self.wait_window(dialog)
            if dialog.result:
                self.task_manager.delete_task(self.selected_task_id)

        self.selected_task_id = None
        self.update_task_list()

    # Recursively delete a task and all its subtasks
    def _delete_task_recursively(self, task_id):
        children = [task for task in self.task_manager.get_all_tasks() if task.parent_id == task_id]
        for child in children:
            self._delete_task_recursively(child.id)
        self.task_manager.delete_task(task_id)

    # Select a task and enable the subtask button
    def select_task(self, task_id):
        self.selected_task_id = task_id
        self.add_subtask_button.configure(state="normal")
        self.update_task_list()

    # Change the status of a task and update the list
    def change_task_status(self, task_id, new_status):
        try:
            self.task_manager.edit_task(task_id, new_status=new_status)
            self.update_task_list()
        except Exception as e:
            ErrorDialog(self, "Error", str(e)) 

    # Filter tasks based on status
    def filter_tasks(self, value):
        self.current_filter = value
        self.update_task_list()

    # Toggle sorting tasks by priority
    def toggle_sort_by_priority(self):
        self.sort_by_priority_enabled = not self.sort_by_priority_enabled
        self.update_task_list()

    # Search for tasks based on the search entry
    def _on_search(self):
        self._search_query = self.search_entry.get().lower()
        self.update_task_list()

    # Apply date range filter based on the date entries
    def _apply_date_filter(self):
        try:
            self._start_date = self.start_date_entry.get_date() if self.start_date_entry.get() else None
            self._end_date = self.end_date_entry.get_date() if self.end_date_entry.get() else None
        except ValueError:
            ErrorDialog(self, "Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        self.update_task_list()

    # Update the task list based on current filters and sorting
    def update_task_list(self):
        # Clear the frame
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        # Fetch and filter tasks
        sort_by = 'priority' if self.sort_by_priority_enabled else None
        all_tasks = self.task_manager.get_all_tasks(sort_by=sort_by, search_query=self._search_query)

        # Apply status filter
        if self.current_filter != "All":
            all_tasks = [task for task in all_tasks if task.status == self.current_filter]

        # Apply date range filter
        if self._start_date and self._end_date:
            all_tasks = [task for task in all_tasks if task.reminder and self._start_date <= task.reminder <= self._end_date]

        # Build a hierarchy
        tasks_by_parent = {None: []}
        for task in all_tasks:
            if task.parent_id not in tasks_by_parent:
                tasks_by_parent[task.parent_id] = []
            tasks_by_parent[task.parent_id].append(task)

        # Recursively display tasks
        self._display_tasks_recursively(None, 0, tasks_by_parent)

    # Export tasks to a file
    def export_tasks_event(self):
        dialog = ExportDialog(self, "Export Tasks")
        self.wait_window(dialog)

        result = dialog.result
        if result:
            file_path, file_format = result
            try:
                self.task_manager.export_tasks(file_path, file_format)
                # Optionally, show a success message
                success_dialog = ConfirmationDialog(self, "Success", f"Tasks successfully exported to {file_path}", show_cancel=False)
                self.wait_window(success_dialog)
            except Exception as e:
                ErrorDialog(self, "Export Error", str(e))

    # Display tasks recursively with indentation for sub-tasks
    def _display_tasks_recursively(self, parent_id, level, tasks_by_parent):
        if parent_id not in tasks_by_parent:
            return

        for task in tasks_by_parent[parent_id]:
            indent = level * 20
            task_frame = ctk.CTkFrame(self.task_list_frame, border_width=1, border_color="gray")
            task_frame.pack(fill="x", pady=2, padx=(5 + indent, 5))

            if task.id == self.selected_task_id:
                task_frame.configure(fg_color=("gray85", "gray15"))

            task_frame.bind("<Button-1>", lambda event, task_id=task.id: self.select_task(task_id))

            reminder_text = f" | Due: {task.reminder.strftime('%Y-%m-%d')}" if task.reminder else ""
            priority_text = f" | Priority: {task.priority}"
            label_text = f"#{task.id}: {task.description}{priority_text}{reminder_text}"

            label = ctk.CTkLabel(task_frame, text=label_text, anchor="w")
            label.pack(side="left", fill="x", expand=True, padx=10)
            label.bind("<Button-1>", lambda event, task_id=task.id: self.select_task(task_id))

            status_menu = ctk.CTkOptionMenu(task_frame, values=["todo", "in-progress", "done"],
                                              command=lambda new_status, task_id=task.id: self.change_task_status(task_id, new_status))
            status_menu.set(task.status)
            status_menu.pack(side="right", padx=10)

            # Recursive call for children
            self._display_tasks_recursively(task.id, level + 1, tasks_by_parent)
