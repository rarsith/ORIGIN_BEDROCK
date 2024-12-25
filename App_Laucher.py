import os
import sys
from PySide2 import QtWidgets
from origin.ui.app_launcher import app_launcher_ui

origin_dev_root = os.getenv("ORIGIN_ROOT")
qss_style_file = os.path.normpath(os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

app = QtWidgets.QApplication(sys.argv)

with open(qss_style_file, "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)

test_dialog = app_launcher_ui.AppLauncher()
test_dialog.setWindowTitle("Application Launcher")
test_dialog.setMinimumHeight(650)
test_dialog.setMinimumWidth(450)

test_dialog.populate_widget()
test_dialog.show()
sys.exit(app.exec_())
