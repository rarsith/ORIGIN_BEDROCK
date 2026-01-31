import os
from importlib import import_module


class DummySessionOps:
    def save_current_file(self):
        print("DummySessionOps.save_current_file() called — no real DCC environment detected.")


def optional_import(full_module_path, fallback=None, verbose=False):
    module_components = full_module_path.rsplit(".", 1)
    try:

        module = import_module(module_components[0])
        return getattr(module, module_components[1])
    except (ModuleNotFoundError, AttributeError):
        if verbose:
            print(f"[optional_import] Module not found: {full_module_path}, skipping import.")
        return fallback


def scene_session_operations_class():
    dcc = os.getenv("DCC")

    dcc_classes = {
        "origin_standalone": DummySessionOps,
        "maya": optional_import("origin.dcc.extensions.maya.files_handler.save_session.MayaSaveSession", fallback=DummySessionOps),
        "houdini": optional_import("origin.dcc.extensions.houdini.save_session.HoudiniSaveSession", fallback=DummySessionOps),
        "blender": optional_import("origin.dcc.extensions.blender.save_session.BlenderSaveSession", fallback=DummySessionOps),
    }

    '''
    if dcc == "maya":
        from origin.dcc.extensions.maya.files_handler.save_session import MayaSaveSession
    elif dcc == "houdini":
        from origin.dcc.extensions.houdini.save_session import HoudiniSaveSession
    elif dcc == "blender":
        from origin.dcc.extensions.blender.save_session import BlenderSaveSession
    else:
        session_class = DummySessionOps
    '''

    session_class = dcc_classes.get(dcc)
    return session_class()


