import importlib
from origin.dcc.extensions.maya.ui.utils.ui_loader import ui_loader
from origin.ui.context_manager_ui import context_manager_ui
importlib.reload(context_manager_ui)


def context_setter():
    ui_loader(main_widget=context_manager_ui.ContextManagerMainUI,
              style_path="origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss",
              size=(100, 100, 700, 300))
