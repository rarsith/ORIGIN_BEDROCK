from envars.envars import Envars
from common_utils.users import Users


class OutputPaths(object):
    def __init__(self, version="", pub_slot="", output_file_name="default"):
        self.version = version
        self.pub_slot = pub_slot
        self.output_file_name = output_file_name

    def base_path(self):
        path_entities = [Envars.show_name,
                         Envars.branch_name,
                         Envars.category,
                         Envars.entry_name,
                         Envars.task_name]
        return path_entities

    def main_publish_path(self):
        base_path = self.base_path()
        main_pub_elements = ["output", self.version, self.pub_slot, self.output_file_name]
        path_entities = base_path+main_pub_elements

        return path_entities

    def original_images_path(self):
        #TODO need to find a way to contain the file image seq with a REGEX pattern
        path_entities = [Envars.show_name,
                         Envars.branch_name,
                         Envars.category,
                         Envars.entry_name,
                         Envars.task_name,
                         "output",
                         self.version,
                         "original",
                         self.pub_slot,
                         self.output_file_name]

        return path_entities

    def review_video_path(self):
        path_entities = [Envars.show_name,
                         Envars.branch_name,
                         Envars.category,
                         Envars.entry_name,
                         "data",
                         Envars.task_name,
                         self.version,
                         self.pub_slot,
                         self.output_file_name]

        return path_entities

    def preview_video_path(self):
        path_entities = [Envars.show_name,
                         Envars.branch_name,
                         Envars.category,
                         Envars.entry_name,
                         "data",
                         Envars.task_name,
                         self.version,
                         self.pub_slot,
                         self.output_file_name]

        return path_entities

    def used_template_path(self):
        pass

    def work_file_path(self):
        path_entities = [Envars.show_name,
                         Envars.branch_name,
                         Envars.category,
                         Envars.entry_name,
                         Envars.task_name,
                         "output",
                         self.version,
                         self.output_file_name]

        return path_entities

    def wip_file_path(self):
        path_entities = [Envars.show_name,
                         Envars.branch_name,
                         Envars.category,
                         Envars.entry_name,
                         Envars.task_name,
                         "users",
                         Users.curr_user(),
                         self.version,
                         self.output_file_name]

        return path_entities

    @staticmethod
    def origin():
        return {'input': 'task/imports_from/slot/version/file.ext', 'link': 'insert_link'}

    @staticmethod
    def compose_db_path_dict(path_entities=[]):
        main_path_all = dict(path_elements=path_entities)
        return main_path_all

    def compose_path(self, path_elements):
        pass
