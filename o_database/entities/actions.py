from abc import ABC, abstractmethod
from o_database.mongo_connection import MongoConnection
from envars.origin_envars import OriginEnvar
from o_database.entities.attributes_paths import DbEntityAttrPath
from o_database.entities.constructors import DbConstructors
from o_database.entities.ids import DbIds
from o_database.schemas.actions import EntityDefaultSchemas

from o_database.entities.operators import (Entity,
                                           CollectionOperators,
                                           Tasks,
                                           Project,
                                           Projects,
                                           WorkFiles,
                                           TaskPublish)

from o_database.mongo import DBFind, DBAdd, DBSet, DBRemove
from o_database.collections.connections import ProjectCollections


class OriginDatabaseCreator(ABC):
    @abstractmethod
    def project(self):
        pass

    @abstractmethod
    def group(self):
        pass

    @abstractmethod
    def asset(self):
        pass

    @abstractmethod
    def tasks(self):
        pass

    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def publishes(self):
        pass


class OriginDatabaseActions(ABC):

    @abstractmethod
    def project(self):
        pass

    @abstractmethod
    def projects(self):
        pass

    @abstractmethod
    def entity(self):
        pass

    @abstractmethod
    def tasks(self):
        pass

    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def publishes(self):
        pass


class OriginBaseActions(OriginDatabaseActions):
    def __init__(self, operand, operation):
        self.db_operand = operand
        self.db_operation = operation

    def project(self):
        return Project(operation=self.db_operand, db_operation=self.db_operation)

    def projects(self):
        return Projects(operation=self.db_operand, db_operation=self.db_operation)

    def entity(self, entity_id=None):
        return Entity(entity_id=entity_id, operation=self.db_operand, db_operation=self.db_operation)

    def tasks(self, entity_id=None):
        return Tasks(entity_id=entity_id, operation=self.db_operand, db_operation=self.db_operation)

    def work(self):
        return WorkFiles(operation=self.db_operand, db_operation=self.db_operation)

    def publishes(self, entity_id=None):
        return TaskPublish(entity_id=entity_id, operation=self.db_operand, db_operation=self.db_operation)


class Query(OriginBaseActions):
    def __init__(self):
        super().__init__(operand=DBFind, operation="attr_values")


class Add(OriginBaseActions):
    def __init__(self):
        super().__init__(operand=DBAdd, operation="value_to_field")


class Set(OriginBaseActions):
    def __init__(self):
        super().__init__(operand=DBSet, operation="attribute_value")


class Remove(OriginBaseActions):
    def __init__(self):
        super().__init__(operand=DBRemove, operation="attribute_value")


class Fetch:

    def project_structure_entities(self):
        return CollectionOperators(ProjectCollections().project_main_collection())

    def project_control_entities(self):
        return CollectionOperators(ProjectCollections().project_control_collection())

    def project_work_entities(self):
        return CollectionOperators(ProjectCollections().project_work_files_collection())

    def project_publish_entities(self):
        return CollectionOperators(ProjectCollections().project_publishes_collection())

    def users_entities(self):
        pass






class Create:
    def __init__(self):
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

        if task_schema is not None:
            save_data["task_schema"] = task_schema

        # try:
        db_collection.insert_one(save_data)

        DBAdd(ProjectCollections().project_main_collection(),
              visual_parent,
              "visual_children").value_to_field(created_id)

        print("{} Group created!".format(name))

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

    def work_session(self, file_name):
        db_collection = self.db[ProjectCollections().project_work_files_collection()]
        created_id, save_data = DbConstructors().work_session_construct(file_name=file_name)

        try:
            db_collection.insert_one(save_data)

            print("{} Work_File created!".format(file_name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def publish(self, version):
        db_collection = self.db[ProjectCollections().project_publishes_collection()]
        created_id, save_data, publish_name = DbConstructors().task_publish_construct(version=version)

        try:
            db_collection.insert_one(save_data)

            print("{} Origin Task Published created!".format(publish_name))
        except Exception as e:
            print("{} Error! Nothing Created!".format(e))


if __name__ == "__main__":
    import random
    from o_database.odb_statuses import DbVersionStatuses
    path_elem = ["assets", "characters"]

    OriginEnvar().show_name = "New_Era"
    OriginEnvar().origin_path_hierarchy = path_elem
    # OriginEnvar().entry_name = "green_hulk"

    tasks = ["modeling", "texturing", "groom", "concept", "rigging", "cfx_set", "fx_set", "sculpting", "surfacing"]
    assets = ["hulk", "red_hulk", "green_hulk", "blue_hulk"]
    pub_statuses = DbVersionStatuses().list_all()

    for pub_ver in range(1, 300):

        task_rand_choice = random.choice(tasks)
        asset_rand_choice = random.choice(assets)
        OriginEnvar().entry_name = asset_rand_choice
        OriginEnvar().task_name = task_rand_choice

        version_string = "{:04d}".format(pub_ver)
        Create().publish(version=version_string)
