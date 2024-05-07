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

    def taget_path(self, *args):
        path = '.'.join(args)
        return path

    def resolve_db_filter(self):
        current_envars = {"show_name": OriginEnvar().show_name,
                          "origin_db_path": OriginEnvar().origin_path_hierarchy,
                          "entry_name": OriginEnvar().entry_name,
                          "task_name": OriginEnvar().task_name}

        db_filter = dict()

        for key, value in current_envars.items():
            if value:
                db_filter[key] = value

        return db_filter

    def _update_hierarchy_path(self, sel_items: list, delimiter=".", use_root=False):
        hierarchy = f"{delimiter}".join([s for s in sel_items if s])
        return hierarchy

    def current_context(self):
        current_envars = {"show_name": OriginEnvar().show_name,
                          "origin_db_path": OriginEnvar().origin_path_hierarchy,
                          "entry_name": OriginEnvar().entry_name,
                          "task_name": OriginEnvar().task_name}

        context = []

        for key, value in current_envars.items():
            if value:
                context.append(value)

        current_context = ".".join(context)

        return current_context

    def resolve_current_context(self):
        current_envars = {"show_name": OriginEnvar().show_name,
                          "origin_db_path": OriginEnvar().origin_path_hierarchy,
                          "entry_name": OriginEnvar().entry_name,
                          "task_name": OriginEnvar().task_name}

        context = []

        for key, value in current_envars.items():
            if value:
                context.append(value)

        current_context = ".".join(context)

        return current_context

    def resolve_context_to_base(self):
        current_envars = {"show_name": OriginEnvar().show_name,
                          "origin_db_path": OriginEnvar().origin_path_hierarchy
                          }

        context = []

        for key, value in current_envars.items():
            if value:
                context.append(value)

        if len(context) == 1:
            return OriginEnvar().show_name
        else:
            current_context = ".".join(context)

        return current_context

    def resolve_entity_id(self):
        current_envars = [OriginEnvar().show_name, OriginEnvar().origin_path_hierarchy, OriginEnvar().entry_name]

        entity_id = ".".join(current_envars)

        return entity_id


if __name__ == "__main__":
    from database import db_connection as mdbconn
    db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]


    selection_list = ["sequences", "XXP", "templates"]

    OriginEnvar.show_name = "Green"
    OriginEnvar.entry_name = "0200"

    OriginEnvar().origin_path_hierarchy = selection_list
    print(OriginEnvar().origin_path_hierarchy)


    # db_filter = OriginEnvar().resolve_db_filter()
    # print(db_filter)


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
        from database import db_connection as mdbconn
        db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]

        if len(sel_names) == 1:
            sel_filter = sel_names[0]
        else:
            sel_filter = ".".join(sel_names)

        pipeline = db_field_startswith("origin_db_path", sel_filter)
        result = list(db["test_extraction"].aggregate(pipeline))

        return result


    def get_document_by_id(doc_id):
        from database import db_connection as mdbconn
        db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]
        cursor = db["test_extraction"].find({"_id": doc_id})
        extract_doc = list(cursor)

        return extract_doc[0]


    def db_update_document_by_id(doc_id, data, field):
        from database import db_connection as mdbconn
        db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]
        db["test_extraction"].update_one({"_id": doc_id}, {"$set": {field: data}})
        return doc_id


    def db_update_parent_document(document: dict, new_parent_id: int) -> dict:
        document["parent"] = new_parent_id
        return document


    def db_recompute_db_document_path(doc_id: int):
        from database import db_connection as mdbconn
        db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]

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


    selected_names = ["TestProject.groupA.groupC.groupF.groupB"]
    docs = get_matching_string_documents(selected_names)
    print(docs)

    # db_reparent_document(5, 3)

    # target_document = get_document_by_id(doc_id = 4)
    # new_parent = db_reparent_document(target_document, new_parent_id=5)
    # adjusted = db_recompute_db_path(5)
    # print(">>>:", target_document)