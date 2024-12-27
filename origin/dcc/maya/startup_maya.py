import importlib
import os

import maya.cmds as cmds
from origin.dcc.env_setup import env_setup
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


def clone_environment():
    from origin.dcc.maya import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT


def add_origin_icons():
    origin_root = os.getenv("ORIGIN_ROOT")
    custom_icon_folder = os.path.join(origin_root, "origin", "icons")
    normalized_path = os.path.normpath(custom_icon_folder)

    unix_path = normalized_path.replace(os.sep, '/')

    if "XBMLANGPATH" in os.environ:
        maya_icons_dir = os.environ["XBMLANGPATH"]
        if unix_path not in maya_icons_dir.split(";"):
            os.environ["XBMLANGPATH"] = maya_icons_dir + unix_path
    else:
        os.environ["XBMLANGPATH"] = unix_path

    if "MAYA_SCRIPT_PATH" in os.environ:
        maya_scripts_dir = os.environ["MAYA_SCRIPT_PATH"]
        if unix_path not in maya_scripts_dir.split(";"):
            os.environ["MAYA_SCRIPT_PATH"] = maya_scripts_dir + unix_path
    else:
        os.environ["MAYA_SCRIPT_PATH"] = unix_path


def set_working_directory(base_directory):
    folders = {
        "scenes": os.path.join(base_directory, "scenes"),
        "caches/alembic": os.path.join(base_directory, "caches", "alembic"),
        "exchange": os.path.join(base_directory, "exchange"),
    }

    for key, folder in folders.items():
        if not os.path.exists(folder):
            os.makedirs(folder)

    cmds.workspace(base_directory, openWorkspace=True)
    cmds.workspace(saveWorkspace=True)
    cmds.workspace(fileRule=["scene", folders["scenes"]])
    cmds.workspace(fileRule=["AlembicCache", folders["caches/alembic"]])
    cmds.workspace(fileRule=["other", folders["exchange"]])

    cmds.optionVar(sv=('lastOpenFileLocation', base_directory))
    cmds.optionVar(sv=('lastOpenSceneLocation', base_directory))
    cmds.optionVar(sv=('lastSaveLocation', base_directory))

    cmds.workspace(saveWorkspace=True)
    cmds.workspace(directory=base_directory)
    cmds.workspace(base_directory, openWorkspace=True)

    print("----> Workspace file rules updated and saved.")
    print(f"----> Workspace set to: {base_directory}")
    print(f"----> Scenes will be saved in: {folders['scenes']}")
    print(f"----> Alembic caches will be saved in: {folders['caches/alembic']}")
    print(f"----> Other exports will be saved in: {folders['exchange']}")

    current_workspace = cmds.workspace(query=True, rootDirectory=True)
    print(f"----> Current workspace root: {current_workspace}")


def set_current_working_directory():
    cloned_env = clone_environment()
    path_ops = OriginOSPathHandler(context=cloned_env)
    add_origin_icons()
    set_working_directory(base_directory=path_ops.work_base_path(as_path=True, abs_path=True))

env_setup()
add_origin_icons()
set_current_working_directory()
