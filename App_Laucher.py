from PySide2 import QtWidgets
from origin.ui.app_launcher import app_launcher_ui

if __name__ == "__main__":
    import sys

    APP_CONFIG_FILE = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\config\applications\config_applications.json"

    qss_style_file = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\origin\ui\style\stylesheets\dark_orange\dark_orange_style.qss"

    app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    test_dialog = app_launcher_ui.AppLauncher(config_file_path=APP_CONFIG_FILE)
    test_dialog.setWindowTitle("Application Launcher")
    test_dialog.setMinimumHeight(650)
    test_dialog.setMinimumWidth(450)

    test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())
