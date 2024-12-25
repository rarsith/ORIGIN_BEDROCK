from abc import ABC, abstractmethod
from origin.database.mongo_connection import MongoConnection
from origin.envars.origin_envars import ContextHandler
from origin.database.entities.constructors import DbConstructors

from origin.database.entities.operators import (Projects,
                                                TaskPublish,
                                                Project,
                                                Asset,
                                                Task, DBAssetVersion
                                                )

from origin.database.mongo import DBFind, DBAdd, DBSet, DBRemove, CollectionOperators

from origin.database.collections.connections import ProjectCollections


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
    def __init__(self, context: ContextHandler = None):
        self.db = MongoConnection().origin_production_database()
        self.applications__db = MongoConnection().origin_setup_database()

        self.context_handler = context
        if self.context_handler is not None:
            self.db_structure_collection = self.db[self.context_handler.show_name]
            self.db_publish_collection = self.db[self.context_handler.project_publishes]
            self.db_work_collection = self.db[self.context_handler.project_work]
            self.db_ops_collection = self.db[self.context_handler.project_control]

        self.db_applications_collection = self.applications__db["Applications"]

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

    def asset_breakdown(self, parent_id):
        save_data = DbConstructors(context=self.context_handler).asset_breakdown_construct(parent_id=parent_id)

        try:
            doc_exists = self.db_publish_collection.find_one({"_id": save_data["_id"]})

            if not doc_exists:
                inserted_data = self.db_publish_collection.insert_one(save_data)

                return inserted_data.inserted_id
            else:
                return save_data["_id"]

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def asset_breakdown_version(self, data):
        save_data = DbConstructors(context=self.context_handler).asset_breakdown_version_construct(input_data=data)

        try:
            doc_exists = self.db_publish_collection.find_one({"_id": save_data["_id"]})

            if not doc_exists:
                inserted_data = self.db_publish_collection.insert_one(save_data)

                return inserted_data.inserted_id
            else:
                return save_data["_id"]

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

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
        doc_exists = self.db_publish_collection.find_one({"_id": db_asset["_id"]})

        if doc_exists is None:
            try:
                inserted_data = self.db_publish_collection.insert_one(db_asset)
                return inserted_data.inserted_id

            except Exception as e:
                print(f"Error {e}, Nothing Done!")

        else:
            return db_asset["_id"]

    def asset_stack(self, parent_id):
        save_data = DbConstructors(context=self.context_handler).asset_stack_construct(parent_id=parent_id)
        doc_exists = self.db_publish_collection.find_one({"_id": save_data["_id"]})

        if doc_exists is None:
            try:
                inserted_data = self.db_publish_collection.insert_one(save_data)

                DBAdd(db_collection=self.context_handler.project_publishes,
                      entry_id=parent_id,
                      attribute="stacks").value_to_field(inserted_data.inserted_id)

                return inserted_data.inserted_id

            except Exception as e:
                print(f"Error {e}, Nothing Done!")

        else:
            return save_data["_id"]

    def asset_stack_version(self, status, db_asset_stream_id=None):
        if db_asset_stream_id is not None:
            if "__" in db_asset_stream_id:
                rebuilt_id = db_asset_stream_id.replace("__", ".")
                self.context_handler.db_asset_stream_id = rebuilt_id
            else:
                self.context_handler.db_asset_stream_id = db_asset_stream_id
        else:
            stack_data_current = DbConstructors(context=self.context_handler).stack_same_data_check()

            if not stack_data_current:
                save_data = DbConstructors(context=self.context_handler).asset_stack_version_construct(status=status)
                doc_exists = self.db_publish_collection.find_one({"_id": save_data["_id"]})
                if not doc_exists:
                    try:
                        inserted_data = self.db_publish_collection.insert_one(save_data)
                        return inserted_data.inserted_id

                    except Exception as e:
                        print(f"Error {e}, Nothing Done!")
                else:
                    return save_data["_id"]

            else:
                print("No Stack Update Needed! Continuing!")

    def db_asset(self, parent, publish_type):
        db_asset = DbConstructors(context=self.context_handler).db_asset_construct(parent_id=parent,
                                                                                   publish_type=publish_type,
                                                                                   task_type=self.context_handler.task_type
                                                                                   )
        doc_exists = self.db_publish_collection.find_one({"_id": db_asset["_id"]})

        if not doc_exists:
            try:
                inserted_data = self.db_publish_collection.insert_one(db_asset)

                return inserted_data.inserted_id
            except Exception as e:
                print(f"Error {e}, Nothing Done!")

        else:
            return db_asset["_id"]

    def asset_stack_version_update(self, status):
        asset_breakdown_resolve = DbConstructors(context=self.context_handler).compile_entity_stack_input_data()

        for db_stream_id in asset_breakdown_resolve:
            self.asset_stack_version(status=status, db_asset_stream_id=db_stream_id)

    def db_asset_version(self,
                         parent_id: str,
                         comment: list,
                         status=None):

        db_asset = DbConstructors(context=self.context_handler).db_asset_version_construct(parent_id=parent_id,
                                                                                           comment=comment,
                                                                                           status=status)

        try:
            inserted_data = self.db_publish_collection.insert_one(db_asset)
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

                print(f"----> Created File Components with ID: {inserted_data.inserted_id}")
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

    def application_entry(self, app_name: str, app_icon: str):
        app_name_display = app_name.capitalize()
        app_db_asset = DbConstructors().db_asset_application(name=app_name_display, app_icon=app_icon)

        try:
            inserted_data = self.db_applications_collection.insert_one(app_db_asset)

            print(f"Created App Entry with ID: {inserted_data.inserted_id}")
            return inserted_data.inserted_id

        except Exception as e:
            print(f"Error {e}, Nothing Done!")

    def application_version_entry(self, parent_id=None,
                                  version_id=None,
                                  exec_path=None,
                                  envars=None,
                                  active=True,
                                  exec_python=None):
        DbConstructors().db_asset_version_application(parent_id=parent_id,
                                                      version_id=version_id,
                                                      active=active,
                                                      exec_path=exec_path,
                                                      exec_python=exec_python,
                                                      envars=envars)


if __name__ == "__main__":
    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'tafer',
                      'entity_id': 'The_Rock.assets.chr.tafe',
                      'asset_breakdown_id': 'The_Rock.assets.chr.tafer.breakdown',
                      'entity_type': 'asset',
                      # 'task_name': "modeling",
                      # 'task_type': "modeling",
                      # 'task_id': "The_Rock.assets.props.knife.modeling",
                      # 'db_asset_id': 'The_Rock.assets.props.knife.geometry.knife_main',
                      # 'db_asset_stream_id': 'The_Rock.assets.props.knife.knife_main',
                      # 'stack_id': 'The_Rock.assets.props.knife.knife_main.asset_stack',
                      }

    context_class = ContextHandler()
    context_class.load_session(session_data=context_sample)

    Create(context=context_class).asset_stack_version_update(status="WIP")
