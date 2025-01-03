import importlib
import os

import maya.cmds as cmds
import maya.mel as mel
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


def load_shelf_from_path(shelf_path):
    if not os.path.exists(shelf_path):
        cmds.warning(f"File not found: {shelf_path}")
        return

    shelf_file_name = os.path.basename(shelf_path).split('.')[0]
    shelf_name = shelf_file_name.split("_")[1]

    top_shelf_layout = mel.eval("$tmp = $gShelfTopLevel;")
    existing_shelves = cmds.shelfTabLayout(top_shelf_layout, query=True, childArray=True)
    if shelf_name in existing_shelves:
        cmds.deleteUI(shelf_name, layout=True)
        cmds.warning(f"Found'{shelf_name}' reloading...")

    try:
        cmds.evalDeferred(lambda: mel.eval(f'source "{shelf_path}";'))

        cmds.evalDeferred(lambda: mel.eval(f'loadNewShelf "{shelf_path}";'))

    except Exception as e:
        cmds.error(f"Failed to load shelf: {e}")


# Example usage


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


def load_origin_maya_shelves(shelves_files_list):
    origin_root = os.getenv("ORIGIN_ROOT")

    for shelf in shelves_files_list:
        custom_shelves_folder = os.path.join(origin_root, "origin", "dcc", "maya", "shelves", shelf)
        normalized_path = os.path.normpath(custom_shelves_folder)
        unix_path = normalized_path.replace(os.sep, '/')
        load_shelf_from_path(shelf_path=unix_path)


def set_working_directory(base_directory):
    folders = {
        "scene_files": os.path.join(base_directory, "scene_files"),
        "caches/alembic": os.path.join(base_directory, "caches", "alembic"),
        "exchange": os.path.join(base_directory, "exchange"),
    }

    for key, folder in folders.items():
        if not os.path.exists(folder):
            os.makedirs(folder)

    cmds.workspace(base_directory, openWorkspace=True)
    cmds.workspace(saveWorkspace=True)
    cmds.workspace(fileRule=["scene", folders["scene_files"]])
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
    print(f"----> Scenes will be saved in: {folders['scene_files']}")
    print(f"----> Alembic caches will be saved in: {folders['caches/alembic']}")
    print(f"----> Other exports will be saved in: {folders['exchange']}")

    current_workspace = cmds.workspace(query=True, rootDirectory=True)
    print(f"----> Current workspace root: {current_workspace}")


def set_current_working_directory():
    cloned_env = clone_environment()
    path_ops = OriginOSPathHandler(context=cloned_env)
    add_origin_icons()
    set_working_directory(base_directory=path_ops.work_base_path(as_path=True, abs_path=True))


maya_shelves = ["shelf_ORIGIN.mel"]

env_setup()
add_origin_icons()

# load_origin_maya_shelves(shelves_files_list=maya_shelves)

set_current_working_directory()
