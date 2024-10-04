from abc import ABC, abstractmethod
from o_database.mongo_connection import MongoConnection
from origin.envars.Xorigin_envars import ContextHandler
from o_database.entities.Xconstructors import DbConstructors

from o_database.entities.Xoperators import (Asset,
                                           CollectionOperators,
                                           Task,
                                           Project,
                                           Projects,
                                            TaskPublish
                                           )


from o_database.mongo import DBFind, DBAdd, DBSet, DBRemove

from o_database.collections.Xconnections import ProjectCollections


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


class OriginBaseActions:
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
        return Project()

    def projects(self):
        return Projects()

    def entity(self, entity_id=None):
        return Asset()

    def tasks(self, entity_id=None):
        return Task()

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

    def __init__(self, project: Project):
        self.project = project

    def project_structure_entities(self):
        return CollectionOperators(ProjectCollections(self.project).project_main_collection())
        # return CollectionOperators("New_Era")

    def project_control_entities(self):
        return CollectionOperators(ProjectCollections(self.project).project_control_collection())

    def project_work_entities(self):
        return CollectionOperators(ProjectCollections(self.project).project_work_files_collection())

    def project_publish_entities(self):
        return CollectionOperators(ProjectCollections(self.project).project_publishes_collection())

    def users_entities(self):
        pass


class Create:
    def __init__(self, context):
        self.db = MongoConnection().origin_production_database()

        self.context_handler = ContextHandler()
        self.context_handler.load_session(context)

        self.db_structure_collection = self.db[self.context_handler.show_name]
        self.db_publish_collection = self.db[self.context_handler.project_publishes]
        self.db_work_collection = self.db[self.context_handler.project_work]
        self.db_ops_collection = self.db[self.context_handler.project_control]

    def create_entity_id(self):
        entity_id = ".".join([self.parent, self.entity_name])
        return entity_id

    def project(self, name, project_type, project_code):
        entity_id = name
        save_data = DbConstructors().project_construct(name=name,
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

    def group(self, name, parent=None):
        if parent is not None:
            create_id = ".".join([parent, name])
        else:
            create_id = ".".join([self.context_handler.show_name, name])
            parent = self.context_handler.show_name

        save_data = DbConstructors().group_construct(name=name,
                                                     entity_id=create_id,
                                                     parent_id=parent
                                                     )

        self.db_structure_collection.insert_one(save_data)

        DBAdd(db_collection=self.context_handler.show_name,
              entry_id=parent,
              attribute="children").value_to_field(create_id)

        print("{} Group created!".format(name))

    def asset(self, name, parent=None, task_schema=None):
        if parent is not None:
            create_id = ".".join([parent, name])
        else:
            create_id = ".".join([self.context_handler.show_name, name])

        save_data = DbConstructors().asset_construct(name=name,
                                                     entity_id=create_id,
                                                     parent_id=parent,
                                                     task_schema=task_schema
                                                     )

        try:
            self.db_structure_collection.insert_one(save_data)

            DBAdd(db_collection=self.context_handler.show_name,
                  entry_id=parent,
                  attribute="children").value_to_field(create_id)

            print("{} Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def task(self, name, parent, task_type):
        if parent is not None:
            create_id = ".".join([parent, name])
        else:
            create_id = ".".join([self.context_handler.show_name, name])

        save_data = DbConstructors().task_construct(name=name,
                                                    entity_id=create_id,
                                                    parent_id=parent,
                                                    task_type=task_type)

        self.db_structure_collection.insert_one(save_data)

    def db_asset(self, parent, name):
        parent_entity = self.context_handler.resolve_to_base_context()
        create_id = ".".join([parent_entity, self.context_handler.task_type, name])

        db_asset = DbConstructors().db_asset_construct(parent_id=parent,
                                                       entity_id=create_id,
                                                       name=name,
                                                       task_type=self.context_handler.task_type
                                                       )

        try:
            inserted_id = self.db_publish_collection.insert_one(db_asset)
            return inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset_version(self,
                         name,
                         entity_id,
                         parent,
                         version=None,
                         status=None):

        db_asset = DbConstructors().db_asset_version_construct(name=name,
                                                               entity_id=entity_id,
                                                               parent_id=parent,
                                                               version=version,
                                                               status=status)
        try:
            inserted_id = self.db_publish_collection.insert_one(db_asset)
            return inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset_file_component(self,
                                entity_id,
                                display_name: str,
                                visibility: bool,
                                file_ext: str,
                                parent_id: str = None,
                                output_file_path: str = None
                                ) -> dict:

        db_asset = DbConstructors().db_asset_file_component(entity_id=entity_id,
                                                            display_name=display_name,
                                                            visibility=visibility,
                                                            file_ext=file_ext,
                                                            parent_id=parent_id,
                                                            output_file_path=output_file_path
                                                            )
        try:
            inserted_id = self.db_publish_collection.insert_one(db_asset)
            return inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def work_session(self, name, entity_id, version, parent_id):
        created_id, save_data = DbConstructors().work_session_construct(name=name,
                                                                        entity_id=entity_id,
                                                                        version=version,
                                                                        parent_id=parent_id)

        try:
            self.db_work_collection.insert_one(save_data)

        except Exception as e:
            print(f"{e} Error! Nothing Done!")

    def publish(self, version):
        created_id, save_data, publish_name = DbConstructors(context=self.context_handler.snapshot_session()).task_publish_construct(version=version)

        try:
            self.db_publish_collection.insert_one(save_data)

            print("{} Origin Task Published created!".format(publish_name))
        except Exception as e:
            print(f"{e} Error! Nothing Created!")


if __name__ == "__main__":
    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr.red_hulk',
                      'entity_name': 'red_hulk',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.red_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling"}

    for i in range(1, 23):
        Create(context=context_sample).publish(version=str(i))
