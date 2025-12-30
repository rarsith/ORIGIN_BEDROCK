import inspect
import os
import sys

from PySide2 import QtWidgets
from PySide2.QtGui import QIcon

from origin.envars.origin_envars import ContextHandler


def _manual_test_context():
    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.props',
                      'entity_name': 'rock',
                      'entity_id': 'The_Rock.assets.props.rock',
                      'asset_breakdown_id': 'The_Rock.assets.props.rock.breakdown',
                      'entity_type': 'asset',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "The_Rock.assets.props.rock.modeling",
                      'db_asset_id': 'The_Rock.assets.props.knife.geometry.rock_main',
                      'db_asset_stream_id': 'The_Rock.assets.props.knife.rock_main',
                      'stack_id': 'The_Rock.assets.props.knife.rock_main.asset_stack',
                      }

    context_obj = ContextHandler()
    context_obj.load_session(session_data=context_sample)


    for key, value in context_sample.items():
        os.environ[key] = value

    return context_obj



def _general_app():
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))


    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    font = app.font()
    font.setPointSize(7)
    app.setFont(font)

    return app


def _window_icon():
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    window_icon_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/icons/origin_tray_icons/origin_tray_v007_32x32.png"))

    return window_icon_file

def test_ui(main_widget, run_app=True, **kwargs):
    app = _general_app()
    context_obj = _manual_test_context()
    window_icon_file = _window_icon()

    sig = inspect.signature(main_widget.__init__)
    if "context" in sig.parameters:
        kwargs["context"] = context_obj

    for k, v in kwargs.items():
        if k in sig.parameters:
            kwargs[k] = v

    test_dialog = main_widget(**kwargs)

    test_dialog.setWindowIcon(QIcon(window_icon_file))
    test_dialog.show()

    if run_app:
        sys.exit(app.exec_())
    else:
        return app, test_dialog


