from common_utils.users import Users
from o_database.utils import attribute_path_utils
from origin.envars.origin_envars import OriginEnvar
from origin.envars.Xorigin_envars import ContextHandler
# from envars.dc_origin_envars import OriginEnvar


class DbIds:
    """
    Takes a list and joins the elements into a string
    Ex: list = ["element1", "element2"] >>>> result > "element1.element2"
    To be used for generating ids for entities at creation time
    """

    def __init__(self):
        self.context_snapshot = OriginEnvar.snapshot_session()
        self.context = ContextHandler()
        self.context.load_session(self.context_snapshot)

    def create_project_id(self, name):
        return attribute_path_utils.make_path("root", name)

    def create_entity_id(self, name):
        entry_id = attribute_path_utils.make_path(self.context.show_name,
                                                  self.context.origin_path_hierarchy,
                                                  name)

        return entry_id

    def create_db_asset_id(self, name):
        entry_id = attribute_path_utils.make_path(self.context.show_name,
                                                  self.context.origin_path_hierarchy,
                                                  self.context.entry_name,
                                                  self.context.task_type,
                                                  "db_asset",
                                                  name,
                                                  )

        return entry_id

    def create_main_pub_id(self, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              self.context.task_name,
                                              "main_pub",
                                              version)

    def create_pub_slot_id(self, pub_slot, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              self.context.task_name,
                                              pub_slot,
                                              version)

    def create_master_bundle_id(self, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              "bundle",
                                              version)

    def create_wip_file_id(self, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              self.context.task_name,
                                              "wip",
                                              version)

    def curr_project_id(self):
        return attribute_path_utils.make_path("root", self.context.show_name)

    def all_in_collection(self):
        return {}

    def curr_entry_id(self):
        entry_id = attribute_path_utils.make_path(self.context.show_name,
                                                  self.context.origin_path_hierarchy,
                                                  self.context.entry_name)
        if entry_id is not None:
            return entry_id

        return ""

    def get_wip_file_id(self, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              self.context.task_name,
                                              Users().curr_user(),
                                              "wip",
                                              version)

    def get_main_pub_id(self, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              self.context.task_name,
                                              "main_pub",
                                              version)

    def get_pub_slot_id(self, pub_slot, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              self.context.task_name,
                                              pub_slot,
                                              version)

    def get_master_bundle_id(self, version):
        return attribute_path_utils.make_path(self.context.show_name,
                                              self.context.origin_path_hierarchy,
                                              self.context.entry_name,
                                              "bundle",
                                              version)


if __name__ == '__main__':
    OriginEnvar.show_name = "BLUE"

    # Envars.entry_name = "circle"
    # Envars.task_name = "rigging"

    cc = DbIds().curr_entry_id()
    print(cc)