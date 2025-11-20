# from origin.ui.loaders_ui.loader_ui import LoaderMainUI
# from origin.envars.origin_envars import ContextHandler
# import importlib
# import GafferUI
#
#
# def clone_environment():
#     from origin.dcc import context_env
#     importlib.reload(context_env)
#
#     NEW_CONTEXT = context_env.get_context_env()
#     CLONED_CONTEXT = ContextHandler()
#     CLONED_CONTEXT.load_session(NEW_CONTEXT)
#     return CLONED_CONTEXT
#
# def origin_loader():
#     # Create Gaffer window
#     gafferWindow = GafferUI.Window("Origin Master")
#
#     current_context = clone_environment()
#
#     widget_add = LoaderMainUI(context=current_context)
#     widget_add.set_style()
#
#
#     # Add widget to the Gaffer window's layout
#     column = GafferUI.ListContainer(GafferUI.ListContainer.Orientation.Vertical)
#     column._qtWidget().layout().addWidget(widget_add)
#
#     gafferWindow.setChild(column)
#     gafferWindow.setVisible(True)
#
#
# GafferUI.ScriptWindow.menuDefinition(application).append( "/ORIGIN/Asset Loader", { "command" : origin_loader } )

from origin.ui.loaders_ui.loader_ui import LoaderMainUI
from origin.envars.origin_envars import ContextHandler
import importlib
import GafferUI

# Persistent reference to prevent garbage collection
window_instance = None


def clone_environment():
    from origin.dcc import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT


def origin_loader():
    global window_instance  # Prevent GC

    gafferWindow = GafferUI.Window("Origin Master")
    current_context = clone_environment()

    widget_add = LoaderMainUI(context=current_context)

    try:
        widget_add.set_style()
    except Exception as e:
        print(f"Error in set_style: {e}")

    column = GafferUI.ListContainer(GafferUI.ListContainer.Orientation.Vertical)

    # Properly wrap Qt widget
    gaffer_widget = GafferUI.Widget(widget_add)
    column.append(gaffer_widget)

    gafferWindow.setChild(column)
    gafferWindow.setVisible(True)

    window_instance = gafferWindow  # Keep reference


# Ensure `application` is valid
if "application" in globals():
    GafferUI.ScriptWindow.menuDefinition(application).append("/ORIGIN/Asset Loader", {"command": origin_loader})
else:
    print("Warning: 'application' is not defined.")

