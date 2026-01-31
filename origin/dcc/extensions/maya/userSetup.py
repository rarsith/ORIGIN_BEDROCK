import maya.utils
import maya.cmds as cmds
from origin.dcc.extensions.maya.bin.post_startup.post_startup_maya import set_origin_maya

if not cmds.commandPort(":4434", query=True):
    cmds.commandPort(name=":4434")

maya.utils.executeDeferred('set_origin_maya()', runOnce=True)
