from contextlib import ContextDecorator
from dataclasses import dataclass
from PySide2.QtCore import QObject, Signal

@dataclass
class Context:
    project: str = ""
    asset: str = ""
    task: str = ""

class ContextManager(ContextDecorator):
    def __init__(self):
        self._context = Context()

    def __enter__(self):
        # Enter context management
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Exit context management
        pass

    def set_context(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self._context, key, value)

    def get_context(self, key):
        return getattr(self._context, key)

    def clear_context(self):
        self._context = Context()

    def get_full_context(self):
        return self._context

# Signal to update context in UI
class ContextUpdater(QObject):
    context_changed = Signal(Context)

# Example usage:
if __name__ == "__main__":
    # Create context manager
    with ContextManager() as context_manager:
        # Simulate UI selection
        selected_project = "ProjectName"
        selected_asset = "AssetName"
        selected_task = "Modeling"

        # Set context
        context_manager.set_context(project=selected_project, asset=selected_asset, task=selected_task)

        # Get current context
        current_context = context_manager.get_full_context()
        print("Current context:", current_context)

        # Clear context if needed
        context_manager.clear_context()
