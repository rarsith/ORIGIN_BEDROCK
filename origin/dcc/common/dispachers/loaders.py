def get_loader_class(dcc):
    dcc_loaders = {}

    if dcc == "maya":
        from origin.dcc.extensions.maya.files_handler.files_loaders import MayaFileHandler
        dcc_loaders[dcc] = MayaFileHandler

    elif dcc == "gaffer":
        from origin.dcc.extensions.gaffer.loaders.gaffer_file_handler import GafferFileHandler
        dcc_loaders[dcc] = GafferFileHandler

    return dcc_loaders.get(dcc)
