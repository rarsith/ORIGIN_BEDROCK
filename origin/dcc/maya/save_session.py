from pathlib import Path

import maya.cmds as cmds

from origin.dcc.maya.exporters.scene.master_scene import MayaMasterSceneExporter
from origin.envars.origin_envars import ContextHandler


class MayaSaveSession:
    def get_current_scene(self):
        return cmds.file(query=True, sceneName=True)

    def check_if_master_opened(self):
        file_path = Path(self.get_current_scene())
        master_directory = Path("origin_scene")

        return master_directory in file_path.parents

    def save_current_file(self):
        current_is_master = self.check_if_master_opened()

        if not current_is_master:
            if cmds.file(query=True, modified=True):
                cmds.file(save=True)
        else:
            print("Current Scene cannot be re-published, master scene already!. Please Save As.. to make it yours!")
            return

        return self.get_current_scene()



