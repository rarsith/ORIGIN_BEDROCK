from abc import ABC, abstractmethod
from origin.o_database.mongo_connection import MongoConnection
from origin.envars.Xorigin_envars import ContextHandler
from origin.o_database.entities.Xconstructors import DbConstructors

from origin.o_database.entities.Xoperators import (CollectionOperators,
                                                   Projects,
                                                   TaskPublish,
                                                   Project,
                                                   Asset,
                                                   Task, DBAssetVersion
                                                   )

from origin.o_database.mongo import DBFind, DBAdd, DBSet, DBRemove

from origin.o_database.collections.Xconnections import ProjectCollections


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
    def __init__(self, context: ContextHandler):
        self.db = MongoConnection().origin_production_database()

        self.context_handler = context

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
            inserted_data = self.db[name].insert_one(save_data)
            self.db.create_collection(name + "__PUBLISHES")
            self.db.create_collection(name + "__WORK")
            self.db.create_collection(name + "__CONTROL")
            print("{} Project created!".format(name))

            return inserted_data.inserted_id

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

        inserted_data = self.db_structure_collection.insert_one(save_data)

        DBAdd(db_collection=self.context_handler.show_name,
              entry_id=parent,
              attribute="children").value_to_field(create_id)

        print("{} Group created!".format(name))

        return inserted_data.inserted_id

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
            inserted_data = self.db_structure_collection.insert_one(save_data)

            DBAdd(db_collection=self.context_handler.show_name,
                  entry_id=parent,
                  attribute="children").value_to_field(create_id)

            print("{} Asset created!".format(name))
            return inserted_data.inserted_id

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

        try:
            inserted_data = self.db_structure_collection.insert_one(save_data)
            return inserted_data.inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset_stream(self, parent, name):
        parent_entity = self.context_handler.resolve_to_base_context()
        create_id = ".".join([parent_entity, name])

        db_asset = DbConstructors().db_asset_stream_construct(parent_id=parent,
                                                              entity_id=create_id,
                                                              name=name,
                                                              )

        try:
            inserted_data = self.db_publish_collection.insert_one(db_asset)
            return inserted_data.inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset(self, parent):
        parent_name = parent.rsplit(".", 1)[1]
        create_id = ".".join([self.context_handler.entity_id, self.context_handler.task_type, parent_name])

        db_asset = DbConstructors().db_asset_construct(parent_id=parent,
                                                       entity_id=create_id,
                                                       task_type=self.context_handler.task_type
                                                       )


        try:
            doc_exists = self.db_publish_collection.find_one({"_id": create_id})

            if not doc_exists:
                inserted_data = self.db_publish_collection.insert_one(db_asset)

                return inserted_data.inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset_version(self,
                         parent_id: str,
                         comment: list,
                         status=None):

        db_asset = DbConstructors(context=self.context_handler).db_asset_version_construct(parent_id=parent_id,
                                                                                           comment=comment,
                                                                                           status=status)

        try:
            inserted_data = self.db_publish_collection.insert_one(db_asset)
            print(f"Created Version with ID: {inserted_data.inserted_id}")
            return inserted_data.inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def db_asset_file_component(self,
                                visibility: bool,
                                file_ext: str,
                                parent_id: str = None,
                                file_path: str = None,
                                db_insert: bool = True,
                                ) -> dict:

        db_asset = DbConstructors(context=self.context_handler).db_asset_file_component(visibility=visibility,
                                                                                        file_ext=file_ext,
                                                                                        parent_id=parent_id,
                                                                                        file_path=file_path
                                                                                        )

        if db_insert:
            try:
                inserted_data = self.db_publish_collection.insert_one(db_asset)

                print(f"Created File Components with ID: {inserted_data.inserted_id}")
                return inserted_data.inserted_id

            except Exception as e:
                print(f"Error {e}, Nothing Done!")

        else:
            return db_asset

    def work_session(self, name, entity_id, version, parent_id):
        created_id, save_data = DbConstructors().work_session_construct(name=name,
                                                                        entity_id=entity_id,
                                                                        version=version,
                                                                        parent_id=parent_id)

        try:
            inserted_data = self.db_work_collection.insert_one(save_data)
            return inserted_data.inserted_id

        except Exception as e:
            print(f"{e} Error! Nothing Done!")

    def publish(self, version):
        created_id, save_data, publish_name = DbConstructors(context=self.context_handler).task_publish_construct(
            version=version)

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

    context_class = ContextHandler()
    context_class.load_session(session_data=context_sample)

    for i in range(1, 23):
        Create(context=context_class).publish(version=str(i))
