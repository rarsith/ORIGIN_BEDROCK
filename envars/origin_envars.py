import os

import o_database.mongo_connection


class OriginEnvar:

    @property
    def os_root(self):
        return os.environ.get('ORIGIN_ROOT')

    @os_root.setter
    def os_root(self, root_path):
        os.environ['ORIGIN_ROOT'] = root_path

    @property
    def entity_id(self):
        return os.environ.get('ENTITY_ID')

    @entity_id.setter
    def entity_id(self, entity_id):
        os.environ['ORIGIN_ID'] = entity_id

    @property
    def entity_type(self):
        return os.environ.get('ENTITY_TYPE')

    @entity_type.setter
    def entity_type(self, entity_type):
        os.environ['ORIGIN_ID'] = entity_type

    @property
    def show_name(self):
        return os.environ.get('ORIGIN_PROJECT')

    @show_name.setter
    def show_name(self, project):
        os.environ['ORIGIN_PROJECT'] = project

    @property
    def project_publishes(self):
        return os.environ.get('ORIGIN_PROJECT_PUBLISHES')

    @project_publishes.setter
    def project_publishes(self, proj_pub):
        os.environ['ORIGIN_PROJECT_PUBLISHES'] = proj_pub

    @property
    def project_work(self):
        return os.environ.get('ORIGIN_PROJECT_WORK')

    @project_work.setter
    def project_work(self, proj_work):
        os.environ['ORIGIN_PROJECT_WORK'] = proj_work

    @property
    def project_control(self):
        return os.environ.get('ORIGIN_PROJECT_CONTROL')

    @project_control.setter
    def project_control(self, proj_ctrl):
        os.environ['ORIGIN_PROJECT_CONTROL'] = proj_ctrl

    @property
    def origin_path_hierarchy(self):
        return os.environ.get('ORIGIN_HIERARCHY')

    @origin_path_hierarchy.setter
    def origin_path_hierarchy(self, selection):
        hierarchy = self._update_hierarchy_path(sel_items=selection)
        os.environ['ORIGIN_HIERARCHY'] = hierarchy

    @property
    def entry_name(self):
        return os.environ.get('ORIGIN_PROJECT_ENTITY')

    @entry_name.setter
    def entry_name(self, entity):
        os.environ['ORIGIN_PROJECT_ENTITY'] = entity

    @property
    def task_name(self):
        return os.environ.get('ORIGIN_ENTITY_TASK')

    @task_name.setter
    def task_name(self, task):
        os.environ['ORIGIN_ENTITY_TASK'] = task

    @property
    def task_type(self):
        return os.environ.get('ORIGIN_TASK_TYPE')

    @task_type.setter
    def task_type(self, task_type):
        os.environ['ORIGIN_TASK_TYPE'] = task_type

    def taget_path(self, *args):
        path = '.'.join(args)
        return path

    def _update_hierarchy_path(self, sel_items: list, delimiter=".", use_root=False):
        hierarchy = f"{delimiter}".join([s for s in sel_items if s])
        return hierarchy

    def current_context(self):
        """
        Returns FULL path, including current task
        """
        current_context = self.resolve_to_full_context()
        return current_context

    def resolve_to_master(self):
        """
        Returns he path to the asset, does not include the task
        """
        to_master = ".".join([OriginEnvar().show_name,
                              OriginEnvar().origin_path_hierarchy,
                              OriginEnvar().entry_name
                              ])

        return to_master

    def resolve_to_full_context(self):
        """
        Returns FULL path, including current task
        """

        context_items = [OriginEnvar().show_name,
                         OriginEnvar().origin_path_hierarchy,
                         OriginEnvar().entry_name,
                         OriginEnvar().task_name]

        check_items_return = [x for x in context_items if x is not None]
        clean_selected = [x for x in check_items_return if len(x) != 0]

        full_context = ".".join(clean_selected)
        return full_context

    def resolve_to_base_context(self):
        """
        Returns the path to the asset, it does not include the asset itself
        """
        if not OriginEnvar().origin_path_hierarchy:
            return OriginEnvar().show_name
        else:

            to_base_context = ".".join([OriginEnvar().show_name,
                                        OriginEnvar().origin_path_hierarchy
                                        ])

            return to_base_context

    def resolve_entity_id(self):
        """
        Returns the composed ID for the entry: to be depricated and replaced
        and replaced with ObjectId()
        """

        resolve_id = self.resolve_to_master()
        return resolve_id

    @classmethod
    def reset_context(cls):
        cls.task_name = None
        cls.entry_name = None
        cls.entity_id = None
        cls.origin_path_hierarchy = None


if __name__ == "__main__":
    selection_list = ["assets", "characters"]

    OriginEnvar.show_name = "New_Era"
    OriginEnvar().origin_path_hierarchy = selection_list
    OriginEnvar.entry_name = "hulk"
    OriginEnvar.task_name = "modeling"
    #

    # print(OriginEnvar().origin_path_hierarchy)

    context = OriginEnvar().resolve_to_full_context()
    print(context)
