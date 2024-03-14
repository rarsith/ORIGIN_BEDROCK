from database.db_connection import MongoConnection
from envars.origin_envars import OriginEnvar
from o_database.entities.attributes_paths import DbEntityAttrPath
from o_database.entities.constructors import DbConstructors
from o_database.entities.ids import DbIds
from o_database.schemas.actions import EntityDefaultSchemas
from o_database.entities.operators import Entity, Assets, CollectionOperators, Tasks, EntityParent, Project, Projects
from o_database.mongo import DBFind, DBAdd, DBSet, DBRemove
from o_database.collections.connections import ProjectCollections


class Query:
    # this to resolve the current context on initiation

    def curr_entity(self):
        return Entity(operation=DBFind, db_operation="attr_values")

    def curr_project(self):
        return Project(operation=DBFind, db_operation="attr_values")

    def projects(self):
        return Projects(operation=DBFind, db_operation="attr_values")

    def curr_asset(self):
        return Assets(operation=DBFind, db_operation="attr_values")

    def curr_task(self):
        return Tasks(operation=DBFind, db_operation="attr_values")

    # def work_files(self):
    #     return WorkFiles(operation=DBFind, db_operation="attr_values")

    # def publishes(self):
    #     return TaskPublish(operation=DBFind, db_operation="attr_values")


class Add:

    def curr_project(self):
        return Project(operation=DBAdd, db_operation="value_to_field")

    # def all_shows(self):
    #     return Projects()

    def curr_asset(self):
        return Assets(operation=DBAdd, db_operation="value_to_field")

    def curr_task(self):
        return Tasks(operation=DBAdd, db_operation="value_to_field")

    # def work_files(self):
    #     return WorkFiles(operation=Add, db_operation="value_to_field")

    # def publishes(self):
    #     return TaskPublish(operation=Add, db_operation="value_to_field")

    def parent(self):
        pass

    def visual_parent(self):
        return EntityParent()


class Set:

    def curr_project(self):
        return Project(operation=DBSet, db_operation="attribute_value")

    # def all_shows(self):
    #     return Projects(operation=Set, db_operation="attribute_value")

    def curr_asset(self):
        return Assets(operation=DBSet, db_operation="attribute_value")

    def curr_task(self):
        return Tasks(operation=DBSet, db_operation="attribute_value")

    # def work_files(self):
    #     return WorkFiles(operation=Set, db_operation="attribute_value")

    # def publishes(self):
    #     return TaskPublish(operation=Set, db_operation="attribute_value")


class Remove:

    def curr_project(self):
        return Project(operation=DBRemove, db_operation="attribute_value")

    # def all_shows(self):
    #     return Projects(operation=Remove, db_operation="attribute_value")

    def curr_asset(self):
        return Assets(operation=DBRemove, db_operation="attribute_value")

    def curr_task(self):
        return Tasks(operation=DBRemove, db_operation="attribute_value")

    # def work_files(self):
    #     return WorkFiles(operation=Remove, db_operation="attribute_value")

    # def publishes(self):
    #     return TaskPublish(operation=Remove, db_operation="attribute_value")


class Fetch:

    def structure_entities(self):
        return CollectionOperators(ProjectCollections().project_main_collection())

    def control_entities(self):
        return CollectionOperators(ProjectCollections().project_control_collection())

    def work_entities(self):
        return CollectionOperators(ProjectCollections().project_work_files_collection())

    def publish_entities(self):
        return CollectionOperators(ProjectCollections().project_publishes_collection())


class Create:

    def __init__(self):
    # this to resolve the current context on initiation
    #     self.db = mdbconn.server[mdbconn.database_name]
        self.db = MongoConnection().origin_production_database()
        self.current_entity_id = DbIds.curr_entry_id()

    def project(self, name, project_type, project_code):
        entity_id = name

        created_id, save_data = DbConstructors().project_construct(name=name,
                                                                   entity_id=entity_id,
                                                                   project_code=project_code,
                                                                   project_type=project_type)

        try:
            self.db[name].insert_one(save_data)
            self.db.create_collection(name + "__PUBLISHES")
            self.db.create_collection(name + "__WORK")
            self.db.create_collection(name + "__CONTROL")
            print("{} Project created!".format(name))

        except ValueError as e:
            print("{} Error! Nothing created!".format(e))

    def group(self, name, task_schema=None):
        db_collection = self.db[OriginEnvar.show_name]
        created_id, save_data, visual_parent = DbConstructors().group_construct(name=name,
                                                                                entity_id=DbIds.create_entity_id(name),
                                                                                task_schema=task_schema
                                                                                )

        # try:
        db_collection.insert_one(save_data)

        DBAdd(ProjectCollections().project_main_collection(),
              visual_parent,
              "visual_children").value_to_field(created_id)

        DBSet(ProjectCollections().project_main_collection(),
              created_id,
              "definition").attribute_value(EntityDefaultSchemas().entry_definition.skeleton_schema)

        print("{} Group created!".format(name))

        # except Exception as e:
        #     print("Error HERE!")
        #     print("{} Error! Nothing Created!".format(e))

    def asset(self, name, task_schema=None):
        db_collection = self.db[OriginEnvar().show_name]
        created_id, save_data, visual_parent = DbConstructors().asset_construct(name=name,
                                                                                entity_id=DbIds.create_entity_id(name),
                                                                                task_schema=task_schema)

        try:
            db_collection.insert_one(save_data)

            DBAdd(ProjectCollections().project_main_collection(),
                visual_parent,
                 "visual_children").value_to_field(created_id)

            DBSet(ProjectCollections().project_main_collection(),
                created_id,
                 "definition").attribute_value(EntityDefaultSchemas().entry_definition.skeleton_schema)

            print("{} Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def task(self, name, task_type):
        task_data = DbConstructors().task_construct(task_type=task_type)

        add_attr = DBAdd(db_collection=OriginEnvar().show_name,
                       entry_id=self.current_entity_id,
                       attribute=DbEntityAttrPath.to_tasks()).attribute_to_document(attr_name=name,
                                                                                     attr_value=task_data)
        return add_attr

    def work_file(self, file_name):
        db_collection = self.db[OriginEnvar().project_work]
        created_id, save_data = DbConstructors().work_session_construct(file_name=file_name)

        try:
            db_collection.insert_one(save_data)

            print("{} Work_File created!".format(file_name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def task_publish(self):
        db_collection = self.db[OriginEnvar().project_publishes]
        created_id, save_data, publish_name = DbConstructors().task_publish_construct()

        try:
            db_collection.insert_one(save_data)

            print("{} Origin Task Published created!".format(publish_name))
        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def origin_ids(self):
        return DbIds()
