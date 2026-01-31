import os
from pathlib import Path

if os.getenv("DCC") == "maya":
    import maya.cmds as cmds

from PySide2 import QtWidgets


class MayaSaveSession:

    @staticmethod
    def get_current_scene():
        return cmds.file(query=True, sceneName=True)

    def check_if_master_opened(self, path=None):
        if path is not None:
            file_path = Path(path)
        else:
            file_path = Path(self.get_current_scene())
        master_directory = "publishes"

        return master_directory in file_path.parts

    def save_current_file(self):
        current_is_master = self.check_if_master_opened()

        if not current_is_master:
            if cmds.file(query=True, modified=True):
                cmds.file(save=True)
        else:
            QtWidgets.QMessageBox.information(self, "WARNING",
                                              "Current Scene cannot be re-published, master scene already!. Please Save As.. to make it yours!")

            return "Current Scene cannot be re-published, master scene already!. Please Save As.. to make it yours!"

        return self.get_current_scene()

if __name__ == "__main__":
    path = r"X:\projects\Small_Rock\assets\characters\tafar\modeling\publishes\data\geometry__tafar__tafar_MAIN\characters__tafar__tafar_MAIN__v0007\origin_scene\characters__tafar__tafar_MAIN__v0007.mb"
    tt = MayaSaveSession()
    xx = tt.check_if_master_opened(path=path)
    print(xx)





