import os
import sys
import time
import subprocess
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QSplashScreen, QLabel
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QThread, QObject, Signal, Qt, QTimer


class BackgroundWorker(QObject):
    finished = Signal()
    update = Signal(str)

    def __init__(self):
        super(BackgroundWorker, self).__init__()

        self.set_root_envar()

    def run(self):
        self.set_root_envar()

    @staticmethod
    def set_root_envar():
        current_file_path = os.path.abspath(__file__)
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        os.environ["ORIGIN_ROOT"] = root_path
        print(f"Environment variable ORIGIN_ROOT set to: {root_path}")


class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.tray_icon_path = None
        self.splash_icon_path = None

        self.setup_envar()

        self.set_style()
        self.start_background_task()

        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon(self.tray_icon_path))  # Replace with your icon file path
        self.tray_icon.setToolTip("Origin VFX")

        self.context_actions()
        self.context_menu()
        self.context_menu_connections()

        self.tray_icon.show()

    def setup_envar(self):
        current_file_path = os.path.abspath(__file__)
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        os.environ["ORIGIN_ROOT"] = root_path
        print(f"Environment variable ORIGIN_ROOT set to: {root_path}")

    def setup_base(self):
        origin_dev_root = os.getenv("ORIGIN_ROOT")
        self.tray_icon_path = os.path.normpath(os.path.join(origin_dev_root, "origin/icons/origin_tray_icons/origin_tray_v007.png"))
        self.splash_icon_path = os.path.normpath(os.path.join(origin_dev_root, "origin/icons/origin_splash_screens/origin_splash_v001.png"))

    def context_menu(self):
        """Creates the context menu for the project tree viewer"""
        self.menu = QMenu()
        self.menu.addAction(self.control_center_action)
        self.menu.addAction(self.app_launcher_action)
        self.menu.addAction(self.data_igest_action)
        self.menu.addSeparator()
        self.menu.addAction(self.publisher_action)
        self.menu.addSeparator()
        self.menu.addAction(self.task_manager_action)
        self.menu.addSeparator()
        self.menu.addAction(self.statistics_action)
        self.menu.addSeparator()
        self.menu.addAction(self.setting_action)
        self.menu.addAction(self.about_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.menu)

    def context_actions(self):
        """Create actions for the context menu."""
        self.control_center_action = QAction("Control Center...")
        self.app_launcher_action = QAction("App Launcher...")
        self.publisher_action = QAction("Publisher...")
        self.data_igest_action = QAction("Data Ingest...")
        self.task_manager_action = QAction("Task Manager...")
        self.statistics_action = QAction("Statistics...")
        self.setting_action = QAction("Settings...")
        self.about_action = QAction("About...")
        self.quit_action = QAction("Quit")

    def context_menu_connections(self):
        self.quit_action.triggered.connect(self.quit)
        self.control_center_action.triggered.connect(self.get_control_center_ui)
        self.statistics_action.triggered.connect(self.action_one_triggered)
        self.app_launcher_action.triggered.connect(self.application_launcher_ui)
        self.setting_action.triggered.connect(self.settings_launcher_ui)

    def get_control_center_ui(self):
        app_launcher_path = os.path.join(os.getenv("ORIGIN_ROOT"), "master.py")
        python_executable = sys.executable  # Path to the current Python interpreter

        try:
            subprocess.Popen([python_executable, app_launcher_path], start_new_session=True)
        except Exception as e:
            print(f"Failed to launch AppLauncher: {e}")

    def application_launcher_ui(self):
        app_launcher_path = os.path.join(os.getenv("ORIGIN_ROOT"), "origin/ui/app_launcher/app_launcher_ui.py")
        python_executable = sys.executable  # Path to the current Python interpreter

        try:
            subprocess.Popen([python_executable, app_launcher_path], start_new_session=True)
        except Exception as e:
            print(f"Failed to launch AppLauncher: {e}")

    def settings_launcher_ui(self):
        app_launcher_path = os.path.join(os.getenv("ORIGIN_ROOT"), "origin/config/settings/settings.py")
        python_executable = sys.executable  # Path to the current Python interpreter

        try:
            subprocess.Popen([python_executable, app_launcher_path], start_new_session=True)
        except Exception as e:
            print(f"Failed to launch Settings: {e}")

    def start_background_task(self):
        """Start a background task in a separate thread."""
        self.thread = QThread()
        self.worker = BackgroundWorker()
        self.setup_base()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.update.connect(self.on_background_update)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    def on_background_update(self, message):
        print(message)

    def action_one_triggered(self):
        env_test = os.getenv("ORIGIN_ROOT")
        print("-----> ORIGIN:  ", env_test)

    def quit(self):
        """Quit the application."""
        print("Quitting application...")
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        self.tray_icon.hide()
        QApplication.quit()

    def perform_loading_tasks(self, status_label):
        tasks = [
            "Initializing modules...",
            "Loading user preferences...",
            "Connecting to the database...",
            "Fetching resources...",
        ]

        for i, task in enumerate(tasks):
            status_label.setText(task)  # Update status label
            QApplication.processEvents()  # Keep UI responsive
            time.sleep(1*0.2)  # Simulate time-consuming task

    def splash_origin(self):
        splash_pix = QPixmap(self.splash_icon_path)  # Replace with your splash image path
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setWindowFlag(Qt.FramelessWindowHint)  # Optional: remove the window border
        splash.show()
        QTimer.singleShot(3000, splash.close)  # Close splash after 3 seconds

        status_label = QLabel("Starting...", splash)
        status_label.setStyleSheet("font-size: 14px; color: black;")
        status_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        status_label.setGeometry(0, 250, 400, 30)

        self.perform_loading_tasks(status_label)

    def run(self):
        splash_pix = QPixmap(self.splash_icon_path)  # Replace with your splash image path
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setWindowFlag(Qt.FramelessWindowHint)  # Optional: remove the window border

        status_label = QLabel("Starting...", splash)
        status_label.setStyleSheet("font-size: 10px; color: #fca80a;")
        status_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        status_label.setGeometry(0, 0, 150, 70)

        splash.show()
        QTimer.singleShot(2000, splash.close)  # Close splash after 3 seconds

        self.perform_loading_tasks(status_label)

        sys.exit(self.app.exec_())

    def set_style(self):
        origin_dev_root = os.getenv("ORIGIN_ROOT")

        qss_style_file = os.path.normpath(
            os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

        with open(qss_style_file, "r") as f:
            _style = f.read()
            self.app.setStyleSheet(_style)

        app_font = self.app.font()
        app_font.setPointSize(10)
        self.app.setFont(app_font)


if __name__ == "__main__":
    app = TrayApp()
    app.run()




