from envars.origin_envars import OriginEnvar


class ProjectCollections:
    def __init__(self):
        self.main_collection_name = OriginEnvar().show_name

    def project_main_collection(self):
        return self.main_collection_name

    def project_work_files_collection(self):
        collection_suffix = "__WORK"
        return self.main_collection_name + collection_suffix

    def project_publishes_collection(self):
        collection_suffix = "__PUBLISHES"
        return self.main_collection_name + collection_suffix

    def project_control_collection(self):
        collection_suffix = "__CONTROL"
        return self.main_collection_name + collection_suffix
