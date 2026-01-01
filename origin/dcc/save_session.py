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
    dcc = os.getenv("DCC", "standalone").lower()

    dcc_classes = {
        "origin_standalone": DummySessionOps,
        "maya": optional_import("origin.dcc.maya.files_handler.save_session.MayaSaveSession", fallback=DummySessionOps),
        "houdini": optional_import("origin.dcc.houdini.save_session.HoudiniSaveSession", fallback=DummySessionOps),
        "blender": optional_import("origin.dcc.blender.save_session.BlenderSaveSession", fallback=DummySessionOps),
    }

    session_class = dcc_classes.get(dcc)  # , DummySessionOps)
    return session_class()
