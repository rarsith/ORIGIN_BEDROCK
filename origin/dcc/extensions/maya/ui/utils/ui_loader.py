import inspect
import os
from typing import Tuple

from PySide2 import QtCore

from origin.dcc.common.utils.context_from_envar import clone_environment
from origin.dcc.extensions.maya.ui.utils.maya_window import get_maya_main_window


def ui_loader(main_widget, style_path, size: Tuple[int, int, int, int], **kwargs):
    current_context = clone_environment()
    context_window_parent = get_maya_main_window()
    origin_root = os.getenv("ORIGIN_ROOT")
    origin_font_size = os.getenv("ORIGIN_FONT_SIZE")

    qss_style_file = os.path.normpath(os.path.join(origin_root, style_path))

    sig = inspect.signature(main_widget.__init__)
    if "context" in sig.parameters:
        kwargs["context"] = current_context

    if "parent" in sig.parameters:
        kwargs["parent"] = context_window_parent

    for k, v in kwargs.items():
        if k in sig.parameters:
            kwargs[k] = v

    window = main_widget(**kwargs)

    try:
        window.setGeometry(*size)
        window.setWindowFlags(QtCore.Qt.Window)

        with open(qss_style_file, "r") as f:
            _style = f.read()
            window.setStyleSheet(_style)

        font = window.font()
        font.setPointSize(int(origin_font_size))
        window.setFont(font)

        window.show()

    except Exception as e:
        print(f"Error occurred: {e}")