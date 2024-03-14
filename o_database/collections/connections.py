from envars.origin_envars import OriginEnvar


class ProjectCollections:

    def project_main_collection(self):
        return OriginEnvar().show_name

    def project_work_files_collection(self):
        collection_suffix = "__WORK"
        return self.project_main_collection() + collection_suffix

    def project_publishes_collection(self):
        collection_suffix = "__PUBLISHES"
        return self.project_main_collection() + collection_suffix

    def project_control_collection(self):
        collection_suffix = "__CONTROL"
        return self.project_main_collection() + collection_suffix
