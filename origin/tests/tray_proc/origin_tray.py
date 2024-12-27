import os
import sys
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PySide2.QtGui import QIcon
from PySide2.QtCore import QThread, QObject, Signal

origin_dev_root = os.getenv("ORIGIN_ROOT")
thumbnail_path = os.path.normpath(os.path.join(origin_dev_root, "origin/icons/pngegg_tray_64x64_golden_stretched.png"))


# Background task in a separate thread
class BackgroundWorker(QObject):
    finished = Signal()
    update = Signal(str)

    def run(self):
        """Simulates a background task."""
        import time
        while True:
            time.sleep(5)
            self.update.emit("Background task is running!")

# Main application
class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon(thumbnail_path))  # Replace with your icon file path
        self.tray_icon.setToolTip("My Tray App")


        self.context_actions()
        self.context_menu()

        # Set the menu for the tray icon

        # Connect to tray icon events
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show the tray icon
        self.tray_icon.show()

        # Start a background task
        self.start_background_task()

    def context_menu(self):
        """Creates the context menu for the project tree viewer"""
        self.menu = QMenu()
        self.menu.addAction(self.create_group_action)
        self.menu.addAction(self.create_asset_action)
        self.menu.addAction(self.edit_entry_definition)
        self.menu.addSeparator()
        self.menu.addAction(self.save_task_schema_action)
        self.menu.addAction(self.assignment_manager_action)
        self.menu.addSeparator()
        self.menu.addAction(self.remove_selected_action)
        self.tray_icon.setContextMenu(self.menu)
        # self.menu.exec_(self.tray_icon.mapToGlobal(point))

    def context_actions(self):
        """Create actions for the context menu."""
        self.about_action = QAction("About")
        self.create_group_action = QAction("Create Group...")
        self.create_asset_action = QAction("Create Asset...")
        self.remove_selected_action = QAction("Remove Selection...")
        self.edit_entry_definition = QAction("Edit Definition...")
        self.save_task_schema_action = QAction("Task Manager...")
        self.assignment_manager_action = QAction("Assignment Manager...")

    def context_menu_connections(self):
        pass
    def start_background_task(self):
        """Start a background task in a separate thread."""
        self.thread = QThread()
        self.worker = BackgroundWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.update.connect(self.on_background_update)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    def on_background_update(self, message):
        """Handle updates from the background task."""
        print(message)

    def action_one_triggered(self):
        """Handle the 'Action 1' menu item."""
        print("Action 1 selected!")

    def on_tray_icon_activated(self, reason):
        """Handle tray icon interactions."""
        if reason == QSystemTrayIcon.Trigger:
            print("Tray icon clicked!")

    def quit(self):
        """Quit the application."""
        print("Quitting application...")
        self.thread.quit()
        self.thread.wait()
        self.tray_icon.hide()
        sys.exit()

    def run(self):
        """Run the application event loop."""
        sys.exit(self.app.exec_())

# Run the application
if __name__ == "__main__":
    app = TrayApp()
    app.run()
