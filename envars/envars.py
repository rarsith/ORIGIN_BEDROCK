import os

from envars.origin_envars import OriginEnvar


class Envars():

    @property
    def os_root(self):
        return os.environ.get('ORIGIN_ROOT')

    @os_root.setter
    def os_root(self, root_path):
        os.environ.get['ORIGIN_ROOT'] = root_path

    @property
    def origin_id(self):
        return os.environ.get('ORIGIN_ID')

    @origin_id.setter
    def origin_id(self, origin_id):
        os.environ['ORIGIN_ID'] = origin_id

    @property
    def show_name(self):
        return os.environ.get('ORIGIN_PROJECT')

    @show_name.setter
    def show_name(self, project):
        os.environ['ORIGIN_PROJECT'] = project

    @property
    def branch_name(self):
        return os.environ.get('ORIGIN_PROJECT_BRANCH')

    @branch_name.setter
    def branch_name(self, branch):
        os.environ['ORIGIN_PROJECT_BRANCH'] = branch

    @property
    def category(self):
        return os.environ.get('ORIGIN_PROJECT_CATEGORY')

    @category.setter
    def category(self, category):
        os.environ['ORIGIN_PROJECT_CATEGORY'] = category

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
    def build_current_master_bundle(self):
        return os.environ.get('ORIGIN_BUILD_MASTER')

    @build_current_master_bundle.setter
    def build_current_master_bundle(self, master_id):
        os.environ['ORIGIN_BUILD_MASTER'] = master_id

    @property
    def shot_current_master_bundle(self):
        return os.environ.get('ORIGIN_SHOT_MASTER')

    @shot_current_master_bundle.setter
    def shot_current_master_bundle(self, master_id):
        os.environ['ORIGIN_SHOT_MASTER'] = master_id

    @property
    def bundle_stream(self):
        return os.environ.get('ORIGIN_BUNDLE_STREAM')

    @bundle_stream.setter
    def bundle_stream(self, stream):
        os.environ['ORIGIN_BUNDLE_STREAM'] = stream

    #needs to be resolved depending on the current pub-ver context
    @property
    def stream_id(self):
        return os.environ.get('ORIGIN_STREAM_ID')

    @stream_id.setter
    def stream_id(self, stream_id):
        os.environ['ORIGIN_STREAM_ID'] = stream_id

    @property
    def stream_full_context(self):
        return os.environ.get('ORIGIN_STREAM_FULL_CONTEXT')

    @stream_full_context.setter
    def stream_full_context(self, stream_full_context):
        os.environ['ORIGIN_STREAM_FULL_CONTEXT'] = stream_full_context

    def taget_path(self, *args):
        path = '.'.join(args)
        return path

    def get_envars_set(self):
        current_envars = {"show_name": Envars().show_name,
                          "branch_name": Envars().branch_name,
                          "category": Envars().category,
                          "entry_name": Envars().entry_name,
                          "task_name": Envars().task_name}

        selection_key = dict()

        for key, value in current_envars.items():
            if value:
                selection_key[key]=value

        return selection_key
    @property
    def project_name(self):
        return os.environ.get('ORIGIN_PROJECT_NAME')

    @project_name.setter
    def project_name(self, proj_name):
        os.environ['ORIGIN_PROJECT_NAME'] = proj_name


if __name__ == "__main__":
    from database import db_connection as mdbconn
    db = mdbconn.server[mdbconn.database_name]

    Envars.show_name = "Green"
    Envars.branch_name = "sequences"
    Envars.category = "XPM"
    Envars.entry_name = "0200"
    Envars.task_name = "animation"

    filter_db = Envars().get_envars_set()
    # print(filter_db)

    cursor = db["shots"].find(filter_db, {"_id": 1})
    # print([x for x in cursor])

    CURRENT_PROJECT = "TestProject"
    documents = [{"_id":1, "name":"TestProject", "type":"project"},
                 {"_id":2, "name":"groupA", "type":"group", "origin_db_path":"TestProject", "parent":1},
                 {"_id":3, "name":"groupB", "type":"group", "origin_db_path":"TestProject.groupA", "parent":2},
                 {"_id":4, "name":"groupC", "type":"group", "origin_db_path":"TestProject.groupA", "parent":2},
                 {"_id":5, "name":"groupD", "type":"group", "origin_db_path":"TestProject.groupA.groupB", "parent":3},
                 {"_id":6, "name":"groupE", "type":"group", "origin_db_path":"TestProject.groupC", "parent":4},
                 {"_id":7, "name":"groupF", "type":"group", "origin_db_path":"TestProject.groupC", "parent":4}]

    from pymongo import MongoClient

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Origin']
    collection = db['test_extraction']
    # collection.insert_many(documents)

    selected_names = [CURRENT_PROJECT, "groupC"]

    list_of_filters = [CURRENT_PROJECT, 1, 2, 3, 6]



