import importlib
from origin.dcc.maya.ui.utils.ui_loader import ui_loader
from origin.ui.loaders_ui import loader_ui
importlib.reload(loader_ui)

def asset_loader():
    ui_loader(main_widget=loader_ui.LoaderMainUI,
              style_path="origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss",
              size=(100, 100, 700, 300))
