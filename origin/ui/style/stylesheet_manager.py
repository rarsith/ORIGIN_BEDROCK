import os

from PySide2.QtWidgets import QApplication


def apply_stylesheet(app: QApplication, stylesheet_path):
    """Apply a stylesheet to the given QApplication."""
    try:
        origin_dev_root = os.getenv("ORIGIN_ROOT")
        qss_style_file = os.path.normpath(os.path.join(origin_dev_root, stylesheet_path))

        with open(stylesheet_path, "r") as f:
            app.setStyleSheet(f.read())

    except Exception as e:
        print(f"Error applying stylesheet: {e}")


def set_font_size_data(app: QApplication, size: int):
    try:
        font = app.font()
        font.setPointSize(size)
        app.setFont(font)

    except Exception as e:
        print(f"Error applying font size: {e}")
