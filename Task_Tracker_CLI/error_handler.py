import traceback
from datetime import datetime

LOG_FILE = "error.log"

class TaskError(Exception):
    """Custom exception for task-related errors."""
    pass

def log_error(exc_type, exc_value, exc_traceback):
    """Logs detailed error information to a file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"--- Error Log: {datetime.now()} ---\n")
        f.write(f"Type: {exc_type.__name__}\n")
        f.write(f"Value: {exc_value}\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        f.write("--- End Log ---\n\n")

def show_error_dialog(manager, message):
    """Displays a TUI error dialog."""
    if manager is None:
        print(f"Fatal error: {message}")
        return

    import pytermgui as ptg

    def close_dialog(*_):
        manager.remove(error_dialog)

    error_dialog = ptg.Window(
        ptg.Label(f"[red]{message}[/red]"),
        ptg.Button("OK", close_dialog, parent_align=ptg.HorizontalAlignment.CENTER),
        width=40,
        box="DOUBLE",
    ).set_title("[red]Error[/red]").center()

    manager.add(error_dialog)
