import os
import sys
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer


class CheckRunEnv(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CheckRunEnv, self).__init__(parent)

        self.message_area = QtWidgets.QTextEdit()
        self.message_area.setReadOnly(True)

        self.close_btn = QtWidgets.QPushButton("Close")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.message_area)
        main_layout.addWidget(self.close_btn)

        self.collect_envars()

    def collect_envars(self):
        user_settings = {
            "ORIGIN_PROJECTS_ROOT": os.getenv("ORIGIN_PROJECTS_ROOT"),
            "ORIGIN_MONGO_URL": os.getenv("ORIGIN_MONGO_URL"),
            "ORIGIN_STUDIO_NAME": os.getenv("ORIGIN_STUDIO_NAME"),
            "ORIGIN_STYLESHEET_SELECT": os.getenv("ORIGIN_STYLESHEET_SELECT"),
            "ORIGIN_INITIAL_SETUP": os.getenv("ORIGIN_INITIAL_SETUP"),
            "ORIGIN_FONT_SIZE": os.getenv("ORIGIN_FONT_SIZE"),
            "ORIGIN_FONT_STYLE": os.getenv("ORIGIN_FONT_STYLE"),
            "ORIGIN_LIB_PROJECT_ROOT": os.getenv("ORIGIN_LIB_PROJECT_ROOT"),
            "ORIGIN_ROOT": os.getenv("ORIGIN_ROOT"),
            "ORIGIN_STYLESHEET_DIR": os.getenv("ORIGIN_STYLESHEET_DIR"),
            "ORIGIN_FONTS_DIR": os.getenv("ORIGIN_FONTS_DIR"),
            "ORIGIN_ICONS_DIR": os.getenv("ORIGIN_ICONS_DIR"),
            "ORIGIN_USD_DIR": os.getenv("ORIGIN_USD_DIR")
        }

        formatted_text = self.format_dict_as_html(user_settings)
        self.message_area.clear()
        QTimer.singleShot(400, lambda: (self.message_area.setHtml(formatted_text)))

    def format_dict_as_html(self, data):
        # Convert dictionary to HTML string with bold keys
        html_lines = ["<b style='color:green;'>Those who seek the path to enlightenment must not be led astray!</b><br>"]
        for envar_name, envar_value in data.items():
            if envar_value is not None or envar_value == "":
                html_lines.append(f"<b>{envar_name}</b>: --> {envar_value}.....<b style='color:green;'>OK</b><br>")
            else:
                html_lines.append(f"<b>{envar_name}</b>: --> {envar_value}.....<b style='color:red;'>Failed</b><br>")

        return "<br>".join(html_lines)


class CheckRunEnvMainUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(CheckRunEnvMainUI, self).__init__(parent)

        self.central_widget = CheckRunEnv()
        self.setWindowTitle(f"Origin Settings")
        self.setCentralWidget(self.central_widget)

        self.setMinimumWidth(600)
        self.setMinimumHeight(450)

        self.create_connections()

    def create_connections(self):
        self.central_widget.close_btn.clicked.connect(lambda: self.close())


if __name__ == "__main__":
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    font = app.font()
    font.setPointSize(7)
    app.setFont(font)

    test_dialog = CheckRunEnvMainUI()
    test_dialog.show()
    sys.exit(app.exec_())
