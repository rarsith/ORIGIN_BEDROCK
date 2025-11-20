import os

from origin.dcc.maya.save_session import MayaSaveSession


def scene_session_operations_class():
    dcc = os.getenv("DCC")

    master_scene_ops = {
        "maya": MayaSaveSession
    }

    return master_scene_ops[dcc]()
