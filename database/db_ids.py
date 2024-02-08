from database.utils import db_path_assembler
from envars.envars import Envars


class DbIds:
    """
    Takes a list and joins the elements into a string
    Ex: list = ["element1", "element2"] >>>> result > "element1.element2"
    To be used for generating ids for entities at creation time
    """

    @classmethod
    def create_project_id(cls, name):
        return db_path_assembler.make_path("root", name)

    @classmethod
    def create_entity_id(cls, name):
        entry_id = db_path_assembler.make_path(Envars.show_name,
                                               Envars.branch_name,
                                               Envars.category,
                                               name)

        return entry_id

    @classmethod
    def create_main_pub_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           Envars.task_name,
                                           "main_pub",
                                           version)

    @classmethod
    def create_pub_slot_id(cls, pub_slot, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           Envars.task_name,
                                           pub_slot,
                                           version)

    @classmethod
    def create_master_bundle_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "bundle",
                                           version)

    @classmethod
    def create_sync_tasks_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "sync_tasks",
                                           version)

    @classmethod
    def create_wip_file_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           Envars.task_name,
                                           "wip",
                                           version)

    @classmethod
    def curr_project_id(cls):
        return db_path_assembler.make_path("root", Envars.show_name)

    @classmethod
    def all_in_collection(cls):
        return {}

    @classmethod
    def curr_entry_id(cls):
        entry_id = db_path_assembler.make_path(Envars.show_name,
                                               Envars.branch_name,
                                               Envars.category,
                                               Envars.entry_name)
        if entry_id is not None:
            return entry_id

        return ""

    @classmethod
    def get_wip_file_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           Envars.task_name,
                                           "wip",
                                           version)

    @classmethod
    def get_main_pub_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           Envars.task_name,
                                           "main_pub",
                                           version)

    @classmethod
    def get_pub_slot_id(cls, pub_slot, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           Envars.task_name,
                                           pub_slot,
                                           version)

    @classmethod
    def get_master_bundle_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "bundle",
                                           version)

    @classmethod
    def get_sync_tasks_id(cls, version):
        return db_path_assembler.make_path(Envars.show_name,
                                           Envars.branch_name,
                                           Envars.category,
                                           Envars.entry_name,
                                           "sync_tasks",
                                           version)


if __name__ == '__main__':
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    # Envars.entry_name = "circle"
    # Envars.task_name = "rigging"

    cc = DbIds().curr_entry_id()
    print(cc)