from PySide2.QtWidgets import QApplication, QSplashScreen, QLabel, QMainWindow, QVBoxLayout, QWidget
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QPixmap
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Main Application", self)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

def perform_loading_tasks(splash, status_label):
    # Simulate loading tasks with dynamic updates
    tasks = [
        "Initializing modules...",
        "Loading user preferences...",
        "Connecting to the database...",
        "Fetching resources...",
        "Finalizing setup...",
    ]

    for i, task in enumerate(tasks):
        status_label.setText(task)  # Update status label
        QApplication.processEvents()  # Keep UI responsive
        time.sleep(1)  # Simulate time-consuming task

if __name__ == "__main__":
    app = QApplication([])

    # Set up the splash screen
    splash_pixmap = QPixmap(400, 300)  # Adjust size as needed
    splash_pixmap.fill(Qt.white)  # Example background
    splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    splash.show()

    # Add a status label to the splash screen
    status_label = QLabel("Starting...", splash)
    status_label.setStyleSheet("font-size: 14px; color: black;")
    status_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
    status_label.setGeometry(0, 250, 400, 30)  # Position it within the splash

    # Perform loading tasks
    perform_loading_tasks(splash, status_label)

    # Close splash screen and show main window
    main_window = MainWindow()
    splash.finish(main_window)
    main_window.show()

    app.exec_()
