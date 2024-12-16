from origin.dcc.maya.loaders.maya_file_handler import MayaFileHandler
# from origin.dcc.blender.loaders.blender_file_handler import BlenderFileHandler

def get_loader_class(dcc):
    dcc_loaders = {
        "maya": MayaFileHandler,
        # "blender": BlenderFileHandler,
      }
    return dcc_loaders.get(dcc)
