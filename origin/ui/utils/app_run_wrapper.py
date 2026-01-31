import importlib
import inspect
import os
import sys

from PySide2 import QtWidgets
from PySide2.QtGui import QIcon

from origin.envars.origin_envars import ContextHandler


def clone_environment():
    from origin.dcc.common.utils import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT

def _general_app():
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    origin_font_size = os.getenv("ORIGIN_FONT_SIZE")
    qss_style_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))


    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    font = app.font()

    if origin_font_size is not None:
        font.setPointSize(int(origin_font_size))
    else:
        font.setPointSize(int(7))

    app.setFont(font)

    return app


def _window_icon():
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    window_icon_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/icons/origin_tray_icons/origin_tray_v007_32x32.png"))

    return window_icon_file


def execute_app(main_widget, run_app=True, widget_size=[300, 800], **kwargs):
    app = _general_app()
    context_obj = clone_environment()
    window_icon_file = _window_icon()

    sig = inspect.signature(main_widget.__init__)
    if "context" in sig.parameters:
        kwargs["context"] = context_obj

    for k, v in kwargs.items():
        if k in sig.parameters:
            kwargs[k] = v

    test_dialog = main_widget(**kwargs)
    test_dialog.setMinimumWidth(widget_size[0])
    test_dialog.setMinimumHeight(widget_size[1])
    test_dialog.setWindowIcon(QIcon(window_icon_file))
    test_dialog.show()

    if run_app:
        sys.exit(app.exec_())
    else:
        return app, test_dialog