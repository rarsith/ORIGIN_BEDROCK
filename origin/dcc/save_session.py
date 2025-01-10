import os

from origin.dcc.maya.save_session import MayaSaveSession


def master_scene_operations_class(context):
    dcc = os.getenv("DCC")

    master_scene_ops = {
        "maya": MayaSaveSession
    }

    return master_scene_ops[dcc](context=context)
