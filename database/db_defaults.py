from envars.envars import Envars
from database.db_ids import DbIds
from database import db_connection as mdbconn


class DbDefaults(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    @property
    def root_definitions(self):
        return "definition"

    @property
    def root_tasks(self):
        return "tasks"

    @property
    def tasks_pub_slot(self):
        return "pub_slot"

    def get_show_defaults(self, default_type):
        root_id = DbIds.curr_project_id()
        query_path = "show_defaults" + "." + (Envars().category + "_" + default_type)
        category_tasks = self.db.show.find({"_id": root_id}, {'_id': 0, query_path: 1})

        for data in category_tasks:
            full_structure = data["show_defaults"][(Envars().category + "_" + default_type)]
            return full_structure

if __name__ == "__main__":
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "red_hulk"
    Envars.task_name = "modeling"


    xx = DbDefaults().get_show_defaults("definition")
    print (xx)