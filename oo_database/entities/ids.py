from common_utils.users import Users
from o_database.utils import attribute_path_utils
from envars.origin_envars import OriginEnvar
# from envars.dc_origin_envars import OriginEnvar


class DbIds:
    """
    Takes a list and joins the elements into a string
    Ex: list = ["element1", "element2"] >>>> result > "element1.element2"
    To be used for generating ids for entities at creation time
    """

    @classmethod
    def create_project_id(cls, name):
        return attribute_path_utils.make_path("root", name)

    @classmethod
    def create_entity_id(cls, name):
        entry_id = attribute_path_utils.make_path(OriginEnvar().show_name,
                                                  OriginEnvar().origin_path_hierarchy,
                                                  name)

        return entry_id

    @classmethod
    def create_main_pub_id(cls, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              OriginEnvar().task_name,
                                              "main_pub",
                                              version)

    @classmethod
    def create_pub_slot_id(cls, pub_slot, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              OriginEnvar().task_name,
                                              pub_slot,
                                              version)

    @classmethod
    def create_master_bundle_id(cls, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              "bundle",
                                              version)

    @classmethod
    def create_wip_file_id(cls, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              OriginEnvar().task_name,
                                              "wip",
                                              version)

    @classmethod
    def curr_project_id(cls):
        return attribute_path_utils.make_path("root", OriginEnvar().show_name)

    @classmethod
    def all_in_collection(cls):
        return {}

    @classmethod
    def curr_entry_id(cls):
        entry_id = attribute_path_utils.make_path(OriginEnvar().show_name,
                                                  OriginEnvar().origin_path_hierarchy,
                                                  OriginEnvar().entry_name)
        if entry_id is not None:
            return entry_id

        return ""

    @classmethod
    def get_wip_file_id(cls, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              OriginEnvar().task_name,
                                              Users().curr_user(),
                                              "wip",
                                              version)

    @classmethod
    def get_main_pub_id(cls, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              OriginEnvar().task_name,
                                              "main_pub",
                                              version)

    @classmethod
    def get_pub_slot_id(cls, pub_slot, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              OriginEnvar().task_name,
                                              pub_slot,
                                              version)

    @classmethod
    def get_master_bundle_id(cls, version):
        return attribute_path_utils.make_path(OriginEnvar().show_name,
                                              OriginEnvar().origin_path_hierarchy,
                                              OriginEnvar().entry_name,
                                              "bundle",
                                              version)


if __name__ == '__main__':
    OriginEnvar.show_name = "BLUE"

    # Envars.entry_name = "circle"
    # Envars.task_name = "rigging"

    cc = DbIds().curr_entry_id()
    print(cc)