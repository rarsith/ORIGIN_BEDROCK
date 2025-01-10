
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds
import os

# Get the scene file from environment variable
scene_file = os.environ.get('Save Scene_OUTPUT', '')
cmds.file(scene_file, open=True, force=True)

# Export ABC
abc_file = "/path/to/output.abc"
cmds.file(exportSelected=True, type='Alembic', force=True)
print(abc_file)
