from database import db_templates
from envars.envars import Envars
from database.utils.db_q_entity import From, QEntity
from database.entities.db_attributes import DbProjectAttrPaths
from database.db_ids import DbIds

class DbProjectBranch(object):

    @staticmethod
    def add_branch(name: str, branch_type: str) -> str:

        QEntity(db_collection=From().projects,
                entry_id=DbIds.curr_project_id(),
                attribute_path=DbProjectAttrPaths.structure()
                ).add_property(name=name,
                               add_data=dict({"type": branch_type}))

        print("{} Origin Branch created!".format(name))
        return name

    @staticmethod
    def get_branches():
        branches = QEntity(db_collection=From().projects,
                           entry_id=DbIds.curr_project_id(),
                           attribute_path=DbProjectAttrPaths.branches()
                           ).get_attr_names()
        return branches

    @property
    def get_current_branch_type(self):
        branch_type = From().current_branch_type()
        return branch_type

    def get_branch_type(self, branch_name):
        branch_type = From().branch_type(branch_name=branch_name)
        return branch_type

    def get_branches_by_type(self, branch_type):
        branches = QEntity(db_collection=From().projects,
                           entry_id=DbIds.curr_project_id(),
                           attribute_path=DbProjectAttrPaths.branches()
                           ).get_attr_names()

        branches_by_type = []
        for branch in branches:
            if self.get_branch_type(branch) == branch_type:
                branches_by_type.append(branch)

        return branches_by_type

    def get_all_entries_in_branch(self, branch_name=Envars.branch_name):
        entries = QEntity(db_collection=From().projects,
                          entry_id=DbIds.curr_project_id(),
                          attribute_path=DbProjectAttrPaths.curr_branch(branch_name=branch_name)
                          ).get_attr_names()

        return entries


class DbAssetCategories(object):

    @staticmethod
    def add_category(name: str, tasks_type: str) -> str:
        category_tasks_type = name + "_tasks"
        category_definition = name + "_definition"

        QEntity(db_collection=From().projects,
                entry_id=DbIds.curr_project_id(),
                attribute_path=DbProjectAttrPaths.curr_branch()
                ).add_property(name=name)

        QEntity(db_collection=From().projects,
                entry_id=DbIds.curr_project_id(),
                attribute_path=DbProjectAttrPaths.show_defaults()
                ).add_property(name=category_tasks_type,
                               add_data=db_templates.tasks_schema(tasks_type))

        QEntity(db_collection=From().projects,
                entry_id=DbIds.curr_project_id(),
                attribute_path=DbProjectAttrPaths.show_defaults()
                ).add_property(name=category_definition,
                               add_data=db_templates.entry_definition(tasks_type))

        print("{} Origin Category created!".format(name))
        return name

    @staticmethod
    def get_categories():
        categories = QEntity(db_collection=From().projects,
                             entry_id=DbIds.curr_project_id(),
                             attribute_path=DbProjectAttrPaths.categories()
                             ).get_attr_names()
        categories.remove("type")
        return categories

    @staticmethod
    def get_all_in_category(category: str):
        all_entries = QEntity(db_collection=From().projects,
                              entry_id=DbIds.curr_project_id(),
                              attribute_path=DbProjectAttrPaths.category_entries(category=category)
                              ).get_attr_names()

        return all_entries



if __name__ == '__main__':
    from envars.envars import Envars

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "hulk"
    Envars.task_name = "surfacing"

    curr_branches = DbProjectBranch().get_branches()
    print (curr_branches)

    current_branch_cat = DbAssetCategories().get_categories()
    print(current_branch_cat)


