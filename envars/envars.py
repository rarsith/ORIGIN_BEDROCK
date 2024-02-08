import os

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
    # Envars.task_name = "animation"

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
    import pprint
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Origin']
    collection = db['test_extraction']
    # collection.insert_many(documents)

    selected_names = [CURRENT_PROJECT, "groupC"]

    list_of_filters = [CURRENT_PROJECT, 1, 2, 3, 6]

    def db_field_startswith(doc_field, sel_filter):
        """
        returns MongoDB filter for aggregation
        it returns the documents that have the field value starting with the inputted :param sel_filter:

        :param sel_filter: ["TestProject", "groupC"]
        :return:
        """
        pipeline = [{"$match": {doc_field: {"$regex": f"^{sel_filter}"}}}]
        return pipeline


    def get_matching_string_documents(sel_names: list) -> list:
        """
        based on the sel_names param, returns a list MongoDB documents (full)
        Example for sel_names param: ""
        :param sel_names:
        :return:
        """
        if len(sel_names) == 1:
            sel_filter = sel_names[0]
        else:
            sel_filter = ".".join(sel_names)

        pipeline = db_field_startswith("origin_db_path", sel_filter)
        result = list(collection.aggregate(pipeline))
        # pprint.pprint(result)
        return result


    def get_document_by_id(doc_id):
        from database import db_connection as mdbconn
        db = mdbconn.server[mdbconn.database_name]
        cursor = db["test_extraction"].find({"_id": doc_id})
        extract_doc = list(cursor)

        return extract_doc[0]


    def db_update_document_by_id(doc_id, data, field):
        from database import db_connection as mdbconn
        db = mdbconn.server[mdbconn.database_name]
        db["test_extraction"].update_one({"_id": doc_id}, {"$set": {field: data}})
        return doc_id


    def db_update_parent_document(document: dict, new_parent_id: int) -> dict:
        document["parent"] = new_parent_id
        return document


    def db_recompute_db_document_path(doc_id: int):
        from database import db_connection as mdbconn
        db = mdbconn.server[mdbconn.database_name]

        parents_id_list = []
        db_path = []

        def get_parent_chain(_id):
            cursor = db["test_extraction"].find({"_id": _id})
            retrieved_doc = [doc for doc in cursor][0]

            if "parent" in retrieved_doc:
                current_parent = retrieved_doc["parent"]
                parent_doc_cursor = db["test_extraction"].find({"_id": current_parent}, {"name":1, "type":1, "parent":1})
                parent_doc = [doc for doc in parent_doc_cursor][0]
                if parent_doc["type"] != "project":
                    if not parent_doc["_id"] in parents_id_list:
                        parents_id_list.insert(0, parent_doc["_id"])
                        db_path.insert(0, parent_doc["name"])
                        get_parent_chain(_id=parents_id_list[0])
                    else:
                        print(f"Not Allowed! Cyclic Operation! Nothing Done!")
                        return
                else:
                    db_path.insert(0, parent_doc["name"])

        get_parent_chain(doc_id)

        return ".".join(db_path)


    def db_reparent_document(doc_id, new_parent):
        target_doc = get_document_by_id(doc_id)
        destination_doc = get_document_by_id(new_parent)
        if target_doc["_id"] != destination_doc["parent"]:
            db_update_document_by_id(doc_id, new_parent, "parent")
            new_origin_path = db_recompute_db_document_path(doc_id)

            db_update_document_by_id(doc_id, new_origin_path, "origin_db_path")

        else:
            print(f"Not Allowed! Cyclic Operation! Nothing Done!. {doc_id} is the PARENT of {new_parent}")
            return


    # get_matching_string_documents(selected_names)

    db_reparent_document(5, 3)

    # target_document = get_document_by_id(doc_id = 4)
    # new_parent = db_reparent_document(target_document, new_parent_id=5)
    # adjusted = db_recompute_db_path(5)
    # print(">>>:", target_document)