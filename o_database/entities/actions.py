from abc import ABC, abstractmethod
from o_database.mongo_connection import MongoConnection
from envars.origin_envars import OriginEnvar
from envars.origin_envars import ContextHandler
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

    def db_execute(self, attribute_path, value=None):
        method = getattr(self.db_operand(db_collection=ProjectCollections().project_main_collection(),
                                         entry_id=self.entity_id,
                                         attribute=attribute_path), self.db_operation)

        if value:
            method(value)
        else:
            return method()

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
    @classmethod
    def attribute_from_document(cls):
        return cls(operand=DBRemove, operation="attribute_from_document")

    @classmethod
    def attribute_value(cls):
        return cls(operand=DBRemove, operation="attribute_value")

    @classmethod
    def value_from_array(cls):
        return cls(operand=DBRemove, operation="value_from_array")


class Fetch:

    def project_structure_entities(self):
        return CollectionOperators(ProjectCollections().project_main_collection())
        # return CollectionOperators("New_Era")

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
        self.current_entity_id = DbIds().curr_entry_id()

        self.context_snapshot = OriginEnvar.snapshot_session()
        self.context = ContextHandler()
        self.context.load_session(self.context_snapshot)

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
                                                                                entity_id=DbIds().create_entity_id(name),
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
        db_collection = self.db[OriginEnvar.show_name]
        created_id, save_data, visual_parent = DbConstructors().asset_construct(name=name,
                                                                                entity_id=DbIds().create_entity_id(name),
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

        add_attr = DBAdd(db_collection=OriginEnvar.show_name,
                         entry_id=self.current_entity_id,
                         attribute=DbEntityAttrPath.to_tasks()).attribute_to_document(attr_name=name,
                                                                                      attr_value=task_data)
        return add_attr

    def db_asset(self, parent_id, name):
        db_collection = self.db[self.context.project_publishes]
        db_asset = DbConstructors().db_asset_construct(parent_id=parent_id,
                                                       entity_id=DbIds().create_db_asset_id(name),
                                                       name=name,
                                                       context=self.context)

        try:
            inserted_id = db_collection.insert_one(db_asset)
            return inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset_version(self,
                         db_asset_id,
                         version=None,
                         pub_comment=None,
                         status=None):

        db_collection = self.db[self.context.project_publishes]
        db_asset = DbConstructors().db_asset_version_construct(parent_id=db_asset_id,
                                                               version=version,
                                                               pub_comment=pub_comment,
                                                               status=status,
                                                               context=self.context)
        try:
            inserted_id = db_collection.insert_one(db_asset)
            return inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset_file_component(self,
                                display_name: str,
                                visibility: bool,
                                file_ext: str,
                                parent_id: str = None,
                                output_file_path: str = None
                                ) -> dict:

        db_collection = self.db[ProjectCollections().project_publishes_collection()]
        db_asset = DbConstructors().db_asset_file_component(display_name=display_name,
                                                            visibility=visibility,
                                                            file_ext=file_ext,
                                                            parent_id=parent_id,
                                                            output_file_path=output_file_path,
                                                            context=self.context)
        try:
            inserted_id = db_collection.insert_one(db_asset)
            return inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def work_session(self, file_name):
        db_collection = self.db[ProjectCollections().project_work_files_collection()]
        created_id, save_data = DbConstructors().work_session_construct(file_name=file_name)

        try:
            db_collection.insert_one(save_data)

            print("{} DBAsset created!".format(file_name))

        except Exception as e:
            print(f"{e} Error! Nothing Done!")

    def publish(self, version):
        db_collection = self.db[ProjectCollections().project_publishes_collection()]
        created_id, save_data, publish_name = DbConstructors().task_publish_construct(version=version)

        try:
            db_collection.insert_one(save_data)

            print("{} Origin Task Published created!".format(publish_name))
        except Exception as e:
            print(f"{e} Error! Nothing Created!")


if __name__ == "__main__":
    import random
    import time
    from o_database.odb_statuses import DbVersionStatuses

    path_elem = ["assets", "chr"]

    OriginEnvar.show_name = "FOX"
    OriginEnvar.origin_path_hierarchy = path_elem
    # OriginEnvar.entry_name = "green_hulk"

    tasks = ["modeling", "texturing", "groom", "concept", "rigging", "cfx_set", "fx_set", "sculpting", "surfacing",
             "scorging"]

    assets = "hulk"

    OriginEnvar.entry_name = assets
    OriginEnvar.task_name = "inital_blocking"
    OriginEnvar.task_type = "modeling"

    pub_statuses = DbVersionStatuses().list_all()

    # for pub_ver in range(1, 500):
    #     task_rand_choice = random.choice(tasks)
    #     asset_rand_choice = random.choice(assets)
    #     OriginEnvar.entry_name = asset_rand_choice
    #     OriginEnvar.task_name = task_rand_choice

        # version_string = "{:04d}".format(pub_ver)
        # Create().publish(version=version_string)
        # time.sleep(1)\

    Create().db_asset(parent_id="test_id", name="body_blocking")
