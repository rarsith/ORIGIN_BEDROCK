import maya.cmds as cmds

from origin.dcc.maya.exporters.scene.master_scene import MayaMasterSceneExporter
from origin.envars.origin_envars import ContextHandler


class MayaSaveSession:
    def __init__(self, context: ContextHandler):

        self.context_handler = context
        self.export_master_scene = MayaMasterSceneExporter(self.context_handler)

    def export_current_file(self):
        if cmds.file(query=True, modified=True):
            cmds.file(save=True)
        published_master_path = self.export_master_scene.execute()
        return published_master_path
        # return cmds.file(query=True, sceneName=True)


