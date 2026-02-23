from origin.common_utils.users import Users
from origin.database.utils import attribute_path_utils


# from envars.dc_origin_envars import OriginEnvar


class DbIds:
    """
    Takes a list and joins the elements into a string
    Ex: list = ["element1", "element2"] >>>> result > "element1.element2"
    To be used for generating ids for entities at creation time
    """

    def __init__(self, context):
        self.context_handler = context

    def create_project_id(self, name):
        return attribute_path_utils.make_path("root", name)

    def create_entity_id(self, name):
        entry_id = attribute_path_utils.make_path(self.context_handler.show_name,
                                                  self.context_handler.origin_path_hierarchy,
                                                  name)

        return entry_id

    def create_db_asset_id(self, name):
        entry_id = attribute_path_utils.make_path(self.context_handler.show_name,
                                                  self.context_handler.origin_path_hierarchy,
                                                  self.context_handler.entity_name,
                                                  self.context_handler.task_type,
                                                  name,
                                                  )

        return entry_id

    def create_main_pub_id(self, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              self.context_handler.task_name,
                                              "main_pub",
                                              version)

    def create_pub_slot_id(self, pub_slot, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              self.context_handler.task_name,
                                              pub_slot,
                                              version)

    def create_master_bundle_id(self, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              "bundle",
                                              version)

    def create_wip_file_id(self, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              self.context_handler.task_name,
                                              "wip",
                                              version)

    def curr_project_id(self):
        return attribute_path_utils.make_path("root", self.context_handler.show_name)

    def get_wip_file_id(self, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              self.context_handler.task_name,
                                              Users().curr_user(),
                                              "wip",
                                              version)

    def get_main_pub_id(self, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              self.context_handler.task_name,
                                              "main_pub",
                                              version)

    def get_pub_slot_id(self, pub_slot, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              self.context_handler.task_name,
                                              pub_slot,
                                              version)

    def get_master_bundle_id(self, version):
        return attribute_path_utils.make_path(self.context_handler.show_name,
                                              self.context_handler.origin_path_hierarchy,
                                              self.context_handler.entity_name,
                                              "bundle",
                                              version)


if __name__ == '__main__':
    from origin.database.entities.operators import WorkFile

    xx = WorkFile(_id="")
    zz = xx.model_dump(by_alias=True)
    print(zz)
