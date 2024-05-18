from typing import Any
from o_database.mongo_connection import MongoConnection
from envars.origin_envars import OriginEnvar
# from envars.dc_origin_envars import OriginEnvar
from o_database.collections.connections import ProjectCollections
from o_database.collections.pipelines import OriginDBPipelines
from o_database.entities.attributes_paths import DbEntityAttrPath, DbTaskAttrPath, DbPubSlotsAttrPath, DbProjectAttrPath
from o_database.entities.ids import DbIds
from o_database.collections.operators import FindInCollection


class Entity:
    def __init__(self, entity_id=None, operation=None, db_operation=None, db_collection=None):
        self.operation = operation
        self.db_operation = db_operation
        self.entity_id = entity_id
        self.db_collection = db_collection

    def _create_op_inst(self, attribute_path, value=None):
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.entity_id,
                                        attribute=attribute_path), self.db_operation)

        if value:
            method(value)
        else:
            return method()

    @property
    def entity_type(self):
        attribute_path = DbEntityAttrPath().to_type()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_type.setter
    def entity_type(self, ent_type):
        attribute_path = DbEntityAttrPath().to_type()
        self._create_op_inst(attribute_path=attribute_path, value=ent_type)

    @property
    def entity_data(self):
        attribute_path = DbEntityAttrPath().to_data()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_data.setter
    def entity_data(self, ent_data):
        attribute_path = DbEntityAttrPath().to_data()
        self._create_op_inst(attribute_path=attribute_path, value=ent_data)

    @property
    def stack_stream(self):
        attribute_path = DbEntityAttrPath().to_stack_stream()
        return self._create_op_inst(attribute_path=attribute_path)

    @stack_stream.setter
    def stack_stream(self, ent_data):
        attribute_path = DbEntityAttrPath().to_stack_stream()
        self._create_op_inst(attribute_path=attribute_path, value=ent_data)

    @property
    def entity_parent(self):
        attribute_path = DbEntityAttrPath().to_parent()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_parent.setter
    def entity_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_parent()
        self._create_op_inst(attribute_path=attribute_path, value=ent_parent)

    @property
    def entity_visual_parent(self):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_visual_parent.setter
    def entity_visual_parent(self, ent_parent):
        attribute_path = DbEntityAttrPath().to_visual_parent()
        self._create_op_inst(attribute_path=attribute_path, value=ent_parent)

    @property
    def entity_name(self):
        attribute_path = DbEntityAttrPath().to_entity_name()
        return self._create_op_inst(attribute_path=attribute_path)

    @entity_name.setter
    def entity_name(self, ent_name):
        attribute_path = DbEntityAttrPath().to_entity_name()
        self._create_op_inst(attribute_path=attribute_path, value=ent_name)

    @property
    def is_active(self):
        attribute_path = DbEntityAttrPath().to_is_active()
        return self._create_op_inst(attribute_path=attribute_path)

    @is_active.setter
    def is_active(self, set_is_active):
        attribute_path = DbEntityAttrPath().to_is_active()
        self._create_op_inst(attribute_path=attribute_path, value=set_is_active)

    @property
    def definition(self):
        attribute_path = DbEntityAttrPath().to_definition()
        return self._create_op_inst(attribute_path=attribute_path)

    @definition.setter
    def definition(self, set_definition):
        attribute_path = DbEntityAttrPath().to_definition()
        self._create_op_inst(attribute_path=attribute_path, value=set_definition)

    @property
    def origin_db_path(self):
        attribute_path = DbEntityAttrPath().to_origin_db_path()
        return self._create_op_inst(attribute_path=attribute_path)

    @origin_db_path.setter
    def origin_db_path(self, set_origin_db_path):
        attribute_path = DbEntityAttrPath().to_tasks()
        self._create_op_inst(attribute_path=attribute_path, value=set_origin_db_path)

    @property
    def children(self):
        attribute_path = DbEntityAttrPath().to_children()
        return self._create_op_inst(attribute_path=attribute_path)

    @children.setter
    def children(self, set_children):
        attribute_path = DbEntityAttrPath().to_tasks()
        self._create_op_inst(attribute_path=attribute_path, value=set_children)

    def all_tasks(self):
        return Tasks(operation=self.operation, db_operation=self.db_operation)

    @property
    def tasks(self):
        attribute_path = DbEntityAttrPath().to_tasks()
        return self._create_op_inst(attribute_path=attribute_path)

    @tasks.setter
    def tasks(self, set_tasks):
        attribute_path = DbEntityAttrPath().to_tasks()
        self._create_op_inst(attribute_path=attribute_path, value=set_tasks)

    @property
    def config(self):
        attribute_path = DbEntityAttrPath().to_config()
        return self._create_op_inst(attribute_path=attribute_path)

    @config.setter
    def config(self, set_config):
        attribute_path = DbEntityAttrPath().to_config()
        self._create_op_inst(attribute_path=attribute_path, value=set_config)

    @property
    def components(self):
        attribute_path = DbEntityAttrPath().to_components()
        return self._create_op_inst(attribute_path=attribute_path)

    @components.setter
    def components(self, set_components):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        self._create_op_inst(attribute_path=attribute_path, value=set_components)

    @property
    def assigned_to(self):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        return self._create_op_inst(attribute_path=attribute_path)

    @assigned_to.setter
    def assigned_to(self, set_assigned_to):
        attribute_path = DbEntityAttrPath().to_assigned_to()
        self._create_op_inst(attribute_path=attribute_path, value=set_assigned_to)


class Groups(Entity):
    def __init__(self, operation=None, db_operation=None):
        super(Groups, self).__init__()
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = DbIds.curr_entry_id()


class Assets(Entity):
    def __init__(self, entity_id=None, operation=None, db_operation=None):
        super(Assets, self).__init__()
        self.operation = operation
        self.db_operation = db_operation
        self.entity_id = entity_id


class CollectionOperators:

    def __init__(self, db_collection=None):
        self.db = MongoConnection().origin_production_database()

        self._limit: Any = None
        self._buffer_list: Any = None
        self._skip_doc: Any = None
        self._sort_documents: Any = None
        self._sort_attribute: Any = None

        if db_collection is None or len(db_collection) == 0:
            self.collection_name = "empty"
        else:
            self.collection_name = db_collection

        self.db_collection = self.db[self.collection_name]

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit: int):
        self._limit = limit

    @property
    def buffer_list(self):
        return self._buffer_list

    @buffer_list.setter
    def buffer_list(self, b_list: list):
        self._buffer_list = b_list

    @property
    def skip_doc(self):
        return self._skip_doc

    @skip_doc.setter
    def skip_doc(self, skip_doc: int):
        self._skip_doc = skip_doc

    @property
    def sort_documents(self):
        return self._sort_documents

    @sort_documents.setter
    def sort_documents(self, value: int):
        self._sort_documents = value

    @property
    def sort_attribute(self):
        return self._sort_attribute

    @sort_attribute.setter
    def sort_attribute(self, attr: str):
        self._sort_attribute = attr

    def root_documents(self, attrib_field, attrib_value):
        ppe = OriginDBPipelines()
        criteria = {attrib_field: attrib_value}
        pipe = ppe.generate_pipeline(criteria)

        try:
            if self.db_collection is not None:
                result_docs = self.db_collection.aggregate(pipe)
                results = ([x for x in result_docs])
                return results
        except Exception as e:
            print(__file__, e)

    def entity_document(self, doc_id):
        db_document = self.db_collection.find_one({"_id": doc_id})
        return db_document

    def entity_children_ids(self, doc_id):
        db_document = self.db_collection.find_one({"_id": doc_id})
        if db_document:
            return db_document.get('visual_children', [])

    def entities_attr_value_starts_with(self, attr_field, val_starts_with):
        orig_pipes = OriginDBPipelines()
        orig_pipes.attribute_field = attr_field
        orig_pipes.value_field = val_starts_with
        orig_pipes.limit_op = self._limit
        orig_pipes.skip_op = self._skip_doc
        orig_pipes.sort_docs = self._sort_documents
        orig_pipes.sort_attr = self._sort_attribute

        criteria = orig_pipes.criteria_value_startswith()
        pipe = orig_pipes.generate_pipeline(criteria)
        try:
            if self.db_collection is not None:
                results = list(self.db_collection.aggregate(pipe))
                return results

        except Exception as e:
            print(__file__, e)

    def entities_with_statuses(self, status: list):
        pass

    def entities_with_owners(self, user_names: list):
        pass

    def entities_with_dates(self, input_dates: list):
        pass

    def entities_with_tasks(self, task_names: list):
        pass

    def entities_with_names(self, entity_names: list):
        pass

    def entities_with_ids(self, entity_ids: list):
        pass

    def tasks_with_start_date(self, entity_ids: list):
        pass

    def tasks_with_end_date(self, entity_ids: list):
        pass

    def entities_with_ids(self, entity_ids: list):
        pass


class ProjectStructureOperations:
    def __init__(self, db_collection=None):
        self.db = MongoConnection().origin_production_database()

        if db_collection is None or len(db_collection) == 0:
            self.collection_name = "empty"
        else:
            self.collection_name = db_collection

        self.db_collection = self.db[self.collection_name]

    def root_children(self):
        ppe = OriginDBPipelines()
        crit = {"visual_parent": f"{self.collection_name}"}
        pipe = ppe.generate_pipeline(crit)

        try:
            if self.db_collection is not None:
                result_docs = self.db_collection.aggregate(pipe)
                results = ([x for x in result_docs])
                return results
        except Exception as e:
            print(__file__, e)


class Tasks:
    def __init__(self, entity_id=None, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.entity_id = entity_id

    def _create_op_inst(self, attribute_path, value=None):
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.entity_id,
                                        attribute=attribute_path), self.db_operation)

        if value:
            method(value)
        else:
            return method()

    def multiple_ops(self, ops_list):
        for operation in ops_list:
            for attr_path, attr_value in operation.items():
                self._create_op_inst(attribute_path=attr_path, value=attr_value)

    def names(self):
        attribute_path = DbEntityAttrPath().to_tasks()
        results = self._create_op_inst(attribute_path=attribute_path)
        return list(results.keys())

    @property
    def is_active(self):
        attribute_path = DbTaskAttrPath().to_is_active()
        return self._create_op_inst(attribute_path=attribute_path)

    @is_active.setter
    def is_active(self, set_active):
        attribute_path = DbTaskAttrPath().to_is_active()
        self._create_op_inst(attribute_path=attribute_path, value=set_active)

    @property
    def user(self):
        attribute_path = DbTaskAttrPath().to_artist()
        return self._create_op_inst(attribute_path=attribute_path)

    @user.setter
    def user(self, set_user):
        attribute_path = DbTaskAttrPath().to_artist()
        self._create_op_inst(attribute_path=attribute_path, value=set_user)

    @property
    def bid_days(self):
        attribute_path = DbTaskAttrPath().to_bid_days()
        return self._create_op_inst(attribute_path=attribute_path)

    @bid_days.setter
    def bid_days(self, set_bid_days):
        attribute_path = DbTaskAttrPath().to_bid_days()
        self._create_op_inst(attribute_path=attribute_path, value=set_bid_days)

    @property
    def end_date(self):
        attribute_path = DbTaskAttrPath().to_end_date()
        return self._create_op_inst(attribute_path=attribute_path)

    @end_date.setter
    def end_date(self, set_end_date):
        attribute_path = DbTaskAttrPath().to_end_date()
        self._create_op_inst(attribute_path=attribute_path, value=set_end_date)

    @property
    def milestones(self):
        attribute_path = DbTaskAttrPath().to_milestones()
        return self._create_op_inst(attribute_path=attribute_path)

    @milestones.setter
    def milestones(self, set_milestones):
        attribute_path = DbTaskAttrPath().to_milestones()
        self._create_op_inst(attribute_path=attribute_path, value=set_milestones)

    @property
    def start_date(self):
        attribute_path = DbTaskAttrPath().to_start_date()
        return self._create_op_inst(attribute_path=attribute_path)

    @start_date.setter
    def start_date(self, set_start_date):
        attribute_path = DbTaskAttrPath().to_start_date()
        self._create_op_inst(attribute_path=attribute_path, value=set_start_date)

    @property
    def worked_days(self):
        attribute_path = DbTaskAttrPath().to_worked_days()
        return self._create_op_inst(attribute_path=attribute_path)

    @worked_days.setter
    def worked_days(self, set_start_date):
        attribute_path = DbTaskAttrPath().to_worked_days()
        self._create_op_inst(attribute_path=attribute_path, value=set_start_date)

    @property
    def previous_artists(self):
        attribute_path = DbTaskAttrPath().to_previous_artists()
        return self._create_op_inst(attribute_path=attribute_path)

    @previous_artists.setter
    def previous_artists(self, set_start_date):
        attribute_path = DbTaskAttrPath().to_previous_artists()
        self._create_op_inst(attribute_path=attribute_path, value=set_start_date)

    @property
    def status(self):
        attribute_path = DbTaskAttrPath().to_status()
        return self._create_op_inst(attribute_path=attribute_path)

    @status.setter
    def status(self, set_status):
        attribute_path = DbTaskAttrPath().to_status()
        self._create_op_inst(attribute_path=attribute_path, value=set_status)

    @property
    def data_schema(self) -> dict:
        attribute_path = DbEntityAttrPath().to_tasks()
        return self._create_op_inst(attribute_path=attribute_path)

    @data_schema.setter
    def data_schema(self, tasks_schema: dict) -> None:
        if self.operation != DBAdd:
            attribute_path = DbEntityAttrPath().to_tasks()
            self._create_op_inst(attribute_path=attribute_path, value=tasks_schema)
        else:
            print(f"Not possible to use {self.operation.__name__}. Use only Set! Nothing DONE")

    @property
    def imports_from(self) -> list:
        attribute_path = DbTaskAttrPath().to_imports_from()
        return self._create_op_inst(attribute_path=attribute_path)

    @imports_from.setter
    def imports_from(self, data_set) -> None:
        attribute_path = DbTaskAttrPath().to_imports_from()
        self._create_op_inst(attribute_path=attribute_path, value=data_set)

    def output_slot(self, name):
        return TaskOutputSlot(operation=self.operation, db_operation=self.db_operation, name=name)

    def output_slots(self):
        return TaskOutputSlot(operation=self.operation, db_operation=self.db_operation)


class TaskOutputSlot:

    def __init__(self, entity_id=None, operation=None, db_operation=None, name=None):
        self.operation = operation
        self.db_operation = db_operation
        self.output_name = name
        self.entity_id = entity_id

    def create_op_inst(self, attribute_path, value=None):
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.entity_id,
                                        attribute=attribute_path), self.db_operation)

        if value:
            method(value)
        else:
            return method()

    @property
    def out_slots_names(self) -> list:
        attribute_path = DbTaskAttrPath().to_pub_slots()
        results = self.create_op_inst(attribute_path=attribute_path)
        return list(results.keys())

    @property
    def data_schema(self):
        attribute_path = DbTaskAttrPath().to_pub_slots()
        return self.create_op_inst(attribute_path=attribute_path)

    @data_schema.setter
    def data_schema(self, full_out_slots_data: dict):
        if self.operation != Add:
            attribute_path = DbTaskAttrPath().to_pub_slots()
            self.create_op_inst(attribute_path=attribute_path, value=full_out_slots_data)
        else:
            print(f"Not possible to use {self.operation.__name__}. Use only Set! Nothing DONE")

    @property
    def type(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_type()
        return self.create_op_inst(attribute_path=attribute_path)

    @type.setter
    def type(self, type_name: str):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_scope()
        self.create_op_inst(attribute_path=attribute_path, value=type_name)

    @property
    def designation(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_scope()
        return self.create_op_inst(attribute_path=attribute_path)

    @designation.setter
    def designation(self, designation_name: str):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_scope()
        self.create_op_inst(attribute_path=attribute_path, value=designation_name)

    @property
    def is_active(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_active()
        return self.create_op_inst(attribute_path=attribute_path)

    @is_active.setter
    def is_active(self, is_active: bool):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_active()
        self.create_op_inst(attribute_path=attribute_path, value=is_active)

    @property
    def reviewable(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_reviewable()
        return self.create_op_inst(attribute_path=attribute_path)

    @reviewable.setter
    def reviewable(self, is_reviewable: bool):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_is_reviewable()
        self.create_op_inst(attribute_path=attribute_path, value=is_reviewable)

    @property
    def used_by(self):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_pub_slot_used_by()
        return self.create_op_inst(attribute_path=attribute_path)

    @used_by.setter
    def used_by(self, input_data):
        attribute_path = DbPubSlotsAttrPath(publish_slot_name=self.output_name).to_pub_slot_used_by()
        self.create_op_inst(attribute_path=attribute_path, value=input_data)


class AssetDefinition:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.current_entity_id = DbIds.curr_entry_id()

    def all(self):
        print("These are all definition elements of current asset")

    def element(self, name):
        print(f"{name} is a definition attribute")


class EntityParent:

    def db(self):
        print("I am the PARENT")

    def visual(self):
        print("I am the VISUAL_PARENT")

    def type(self):
        print("I am the TYPE")

    def add_to_visual_parent(self):
        pass


class Project:

    def __init__(self, entity_id=None, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.entity_id = entity_id

    def _create_op_inst(self, attribute_path, value=None):
        method = getattr(self.operation(db_collection=ProjectCollections().project_main_collection(),
                                        entry_id=self.entity_id,
                                        attribute=attribute_path), self.db_operation)

        if value:
            method(value)
        else:
            return method()

    @property
    def project_type(self):
        attribute_path = DbProjectAttrPath().to_type()
        return self._create_op_inst(attribute_path=attribute_path)

    @project_type.setter
    def project_type(self, set_type):
        attribute_path = DbProjectAttrPath().to_type()
        self._create_op_inst(attribute_path=attribute_path, value=set_type)

    @property
    def code(self):
        attribute_path = DbProjectAttrPath().to_code()
        return self._create_op_inst(attribute_path=attribute_path)

    @code.setter
    def code(self, set_code):
        attribute_path = DbProjectAttrPath().to_code()
        self._create_op_inst(attribute_path=attribute_path, value=set_code)

    @property
    def is_active(self):
        attribute_path = DbProjectAttrPath().to_is_active()
        return self._create_op_inst(attribute_path=attribute_path)

    @is_active.setter
    def is_active(self, set_is_active):
        attribute_path = DbProjectAttrPath().to_is_active()
        self._create_op_inst(attribute_path=attribute_path, value=set_is_active)

    @property
    def project_configuration(self) -> dict:
        attribute_path = DbProjectAttrPath().to_project_configuration()
        return self._create_op_inst(attribute_path=attribute_path)

    @project_configuration.setter
    def project_configuration(self, config_data: dict):
        attribute_path = DbProjectAttrPath().to_project_configuration()
        self._create_op_inst(attribute_path=attribute_path, value=config_data)

    @property
    def project_data(self):
        attribute_path = DbProjectAttrPath().to_data()
        return self._create_op_inst(attribute_path=attribute_path)

    @project_data.setter
    def project_data(self, set_data):
        attribute_path = DbProjectAttrPath().to_data()
        self._create_op_inst(attribute_path=attribute_path, value=set_data)


class Projects:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation

    def names(self):
        delimiter = "__"

        projects_list = []
        get_all_in_database = FindInCollection().all_collections()
        for db_collection in get_all_in_database:
            if delimiter not in db_collection:
                projects_list.append(db_collection)

        return projects_list


class WorkFiles:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.db_collection = ProjectCollections().project_work_files_collection()
        # self.current_entity_id = DbIds.curr_entry_id()

    def all(self):
        print("These are all Work Files")

    def by_user(self):
        pass

    def by_date(self):
        pass

    def curr_task(self):
        pass

    def outdated_inputs(self):
        pass

    def my_work_files(self):
        pass


class TaskPublish:
    def __init__(self, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation

    def all(self, limit=None):
        print("These are all publishes")

    def task(self):
        pass

    def owner(self):
        pass

    def date(self):
        pass

    def time(self):
        pass

    def status(self):
        pass

    def components(self):
        pass

    def thumbnail(self):
        pass

    def version(self):
        pass
