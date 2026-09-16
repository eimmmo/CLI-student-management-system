import customtkinter as ctk
from tkinter import filedialog
from tkcalendar import DateEntry

# Error dialog with a message and OK button
class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.message = message

        self.message_label = ctk.CTkLabel(self, text=self.message, wraplength=350)
        self.message_label.pack(pady=20, padx=20)

        self.ok_button = ctk.CTkButton(self, text="OK", command=self.destroy)
        self.ok_button.pack(pady=10)

# Confirmation dialog that returns True or False based on user choice
class ConfirmationDialog(ctk.CTkToplevel):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.message = message
        self.result = False

        self.message_label = ctk.CTkLabel(self, text=self.message)
        self.message_label.pack(pady=20, padx=20)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.yes_button = ctk.CTkButton(self.button_frame, text="Yes", command=self.on_yes)
        self.yes_button.pack(side="left", padx=10)

        self.no_button = ctk.CTkButton(self.button_frame, text="No", command=self.on_no)
        self.no_button.pack(side="left", padx=10)

    def on_yes(self):
        self.result = True
        self.destroy()

    def on_no(self):
        self.result = False
        self.destroy()

# Dialog to export tasks as a CSV file
class ExportDialog(ctk.CTkToplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.result = None

        self.format_label = ctk.CTkLabel(self, text="Export tasks to CSV file:")
        self.format_label.pack(pady=(10, 0))

        self.export_button = ctk.CTkButton(self, text="Export", command=self.export)
        self.export_button.pack(pady=20)

    def export(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV File"
        )
        if file_path:
            self.result = (file_path, "CSV")
            self.destroy()

# Dialog to create or edit a task
class TaskDialog(ctk.CTkToplevel):
    def __init__(self, master, title, task_manager, task=None, parent_id=None):
        super().__init__(master)
        self.title(title)
        self.task_manager = task_manager
        self.task = task
        self.result = None
        self.preselected_parent_id = parent_id

        # Description input
        self.description_label = ctk.CTkLabel(self, text="Description:")
        self.description_label.pack(pady=(10, 0))
        self.description_entry = ctk.CTkEntry(self, width=300)
        self.description_entry.pack(pady=5, padx=20)

        # Reminder input (optional)
        self.reminder_label = ctk.CTkLabel(self, text="Reminder (optional):")
        self.reminder_label.pack(pady=(10, 0))
        self.reminder_entry = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.reminder_entry.pack(pady=5, padx=20)

        # Priority dropdown
        self.priority_label = ctk.CTkLabel(self, text="Priority:")
        self.priority_label.pack(pady=(10, 0))
        self.priority_menu = ctk.CTkOptionMenu(self, values=["Low", "Medium", "High"])
        self.priority_menu.pack(pady=5, padx=20)

        # Parent task dropdown (optional)
        self.parent_label = ctk.CTkLabel(self, text="Parent Task (optional):")
        self.parent_label.pack(pady=(10, 0))

        self.tasks_for_dropdown = {"None": None}
        all_tasks = self.task_manager.get_all_tasks()
        for t in all_tasks:
            if self.task and t.id == self.task.id:
                continue
            self.tasks_for_dropdown[f"#{t.id}: {t.description[:30]}..."] = t.id

        self.parent_menu = ctk.CTkOptionMenu(self, values=list(self.tasks_for_dropdown.keys()))
        self.parent_menu.pack(pady=5, padx=20)

        # Pre-fill fields if editing an existing task
        if self.task:
            self.description_entry.insert(0, self.task.description)
            if self.task.reminder:
                self.reminder_entry.set_date(self.task.reminder)
            self.priority_menu.set(self.task.priority)

            current_parent_id = self.task.parent_id
            if current_parent_id:
                for text, pid in self.tasks_for_dropdown.items():
                    if pid == current_parent_id:
                        self.parent_menu.set(text)
                        break
            else:
                self.parent_menu.set("None")
        elif self.preselected_parent_id:
            for text, pid in self.tasks_for_dropdown.items():
                if pid == self.preselected_parent_id:
                    self.parent_menu.set(text)
                    break

        # Save button
        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_task)
        self.save_button.pack(pady=20)

    def save_task(self):
        description = self.description_entry.get()
        reminder = self.reminder_entry.get_date().strftime('%Y-%m-%d') if self.reminder_entry.get() else None
        priority = self.priority_menu.get()
        selected_parent_text = self.parent_menu.get()
        parent_id = self.tasks_for_dropdown.get(selected_parent_text)

        try:
            if self.task:
                self.task_manager.edit_task(self.task.id, new_description=description, new_reminder=reminder, new_priority=priority, new_parent_id=parent_id)
            else:
                self.task_manager.add_task(description, reminder, priority, parent_id=parent_id)
            
            self.master.update_task_list()
            self.destroy()
        except Exception as e:
            ErrorDialog(self, "Error", str(e))
