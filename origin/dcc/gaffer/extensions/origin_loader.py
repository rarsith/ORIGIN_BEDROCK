from origin.ui.loaders_ui.loader_ui import LoaderMainUI
from origin.envars.origin_envars import ContextHandler
import importlib
import GafferUI
from PySide2 import QtWidgets

def clone_environment():
    from origin.dcc import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT

def origin_loader():
    # Create Gaffer window
    gafferWindow = GafferUI.Window("Origin Master")

    current_context = clone_environment()

    widget_add = LoaderMainUI(context=current_context)
    widget_add.set_style()


    # Add widget to the Gaffer window's layout
    column = GafferUI.ListContainer(GafferUI.ListContainer.Orientation.Vertical)
    column._qtWidget().layout().addWidget(widget_add)

    gafferWindow.setChild(column)
    gafferWindow.setVisible(True)


GafferUI.ScriptWindow.menuDefinition(application).append( "/ORIGIN/Asset Loader", { "command" : origin_loader } )
