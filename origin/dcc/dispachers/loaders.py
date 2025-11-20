

# from origin.dcc.blender.loaders.blender_file_handler import BlenderFileHandler

def get_loader_class(dcc):
    dcc_loaders = {}

    if dcc == "maya":
        from origin.dcc.maya.loaders.maya_file_handler import MayaFileHandler
        dcc_loaders[dcc] = MayaFileHandler

    elif dcc == "gaffer":
        from origin.dcc.gaffer.loaders.gaffer_file_handler import GafferFileHandler
        dcc_loaders[dcc] = GafferFileHandler

    # dcc_loaders = {
    #     "maya": MayaFileHandler,
    #     "gaffer": GafferFileHandler,
    #     # "blender": BlenderFileHandler,
    #   }
    return dcc_loaders.get(dcc)
