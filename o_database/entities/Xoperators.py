from typing import Any, List, Union, Dict
from o_database.mongo_connection import MongoConnection
from o_database.collections.Xconnections import ProjectCollections
from o_database.collections.pipelines import OriginDBPipelines

from o_database.collections.operators import FindInCollection
from pydantic import BaseModel, Field
from typing import Optional, ClassVar
from o_database.mongo import DBSet, DBAdd


def get_entity_class(item_type):
    if item_type == "group":
        return Group
    if item_type == "asset":
        return Asset
    if item_type == "project":
        return Project
    if item_type == "task":
        return Task


class PublishOptions(BaseModel):
    PARENT_DB_ASSET_ID: ClassVar[str] = "parent_db_asset_id"
    parent_db_asset_id: Optional[str] = None

    QUALITY_CHECKS: ClassVar[str] = "quality_checks"
    quality_checks: Optional[str] = None

    FILE_FORMATS: ClassVar[list] = "file_formats"
    file_formats: Optional[list] = None

    COLLECTIONS: ClassVar[dict] = "collections"
    collections: Optional[dict] = None

    REVIEW_OPTIONS: ClassVar[list] = "review_options"
    review_options: Optional[list] = None

    ADDITIONAL_OPERATIONS: ClassVar[list] = "additional_operations"
    additional_operations: Optional[list] = None

    BUNDLE_STREAM_ID: ClassVar[str] = "bundle_stream_id"
    bundle_stream_id: Optional[str] = None

    PUBLISH_COMMENT_ID: ClassVar[str] = "publish_comment_id"
    publish_comment_id: Optional[str] = None

    PUBLISH_STATUS: ClassVar[str] = "publish_status"
    publish_status: Optional[str] = None


class _EntityBaseModel(BaseModel):
    ID: ClassVar[str] = "_id"
    id: Optional[str] = Field(alias='_id')

    NAME: ClassVar[str] = "name"
    name: Optional[str] = None

    ACTIVE: ClassVar[bool] = "active"
    active: Optional[bool] = None

    TYPE: ClassVar[str] = "type"
    type: Optional[str] = None

    PARENT: ClassVar[str] = "parent"
    parent: Optional[str] = None

    CHILDREN: ClassVar[list] = "children"
    children: Optional[list] = None

    ORIGIN_DB_PATH: ClassVar[str] = "origin_db_path"
    origin_db_path: Optional[str] = None

    DATE: ClassVar[str] = "date"
    date: Optional[str] = None

    TIME: ClassVar[str] = "time"
    time: Optional[str] = None

    OWNER: ClassVar[str] = "owner"
    owner: Optional[str] = None

    STATUS: ClassVar[str] = "status"
    status: Optional[str] = None

    COMPONENTS: ClassVar[str] = "components"
    components: Optional[dict] = None

    model_config = {
        "from_attributes": True,
    }

    def parent_show(self):
        delimiter = "."

        if delimiter not in self.id:
            return self.id

        parent_show = self.id.split(delimiter, 1)[0]
        return parent_show

    def project_control_collection(self):
        parent_show = self.parent_show()
        proj_control = "__".join([parent_show, "CONTROL"])
        return proj_control

    def project_publishes_collection(self):
        parent_show = self.parent_show()
        proj_publishes = "__".join([parent_show, "PUBLISHES"])
        return proj_publishes

    def project_work_collection(self):
        parent_show = self.parent_show()
        proj_work = "__".join([parent_show, "WORK"])
        return proj_work

    def get_parent(self):
        parent_id = self.id.rsplit(".", 1)[0]
        doc_data = CollectionOperators(db_collection=self.parent_show())
        db_doc = doc_data.entity_document(doc_id=parent_id)
        return _EntityBaseModel(**db_doc)

    def set_parent(self, parent):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.PARENT).attribute_value(data=parent)

    def get_children(self):
        children = []
        doc_data = CollectionOperators(db_collection=self.parent_show())
        children_docs = doc_data.children_with_parent_id(parent_id=self.id)
        for child in children_docs:
            children.append(child)
        return children

# Trying something
    def db_operations(self):
        return CollectionOperators(db_collection=self.parent_show())


class Task(_EntityBaseModel):
    TASK_TYPE: ClassVar[str] = None
    task_type: Optional[str] = None

    ARTIST: ClassVar[str] = None
    artist: Optional[str] = None

    IMPORTS_FROM: ClassVar[dict] = None
    imports_from: Optional[dict] = None

    BID_DAYS: ClassVar[str] = None
    bid_days: Optional[str] = None

    END_DATE: ClassVar[str] = None
    end_date: Optional[str] = None

    MILESTONES: ClassVar[dict] = None
    milestones: Optional[dict] = None

    START_DATE: ClassVar[str] = None
    start_date: Optional[str] = None

    WORKED_DAYS: ClassVar[str] = None
    worked_days: Optional[str] = None

    PRIORITY: ClassVar[str] = None
    priority: Optional[str] = None

    DESCRIPTION: ClassVar[str] = None
    description: Optional[str] = None

    PREVIOUS_ARTISTS: ClassVar[list] = None
    previous_artists: Optional[list] = None

    def set_artist(self, data: str):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.ARTIST).attribute_value(data=data)

    def add_imports_from(self, data: dict):
        DBAdd(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.IMPORTS_FROM).value_to_field(data=data)

    def set_bid_days(self, data: str):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.BID_DAYS).attribute_value(data=data)

    def set_end_date(self, data: str):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.END_DATE).attribute_value(data=data)

    def add_milestones(self, data: dict):
        DBAdd(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.MILESTONES).value_to_field(data=data)

    def set_start_date(self, data: str):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.START_DATE).attribute_value(data=data)

    def set_worked_days(self, data: str):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.WORKED_DAYS).attribute_value(data=data)

    def add_previous_artists(self, data: str):
        DBAdd(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.PREVIOUS_ARTISTS).value_to_field(data=data)


class Group(_EntityBaseModel):
    DATA: ClassVar[dict] = "data"
    data: Optional[dict] = None


class Asset(_EntityBaseModel):
    DEFINITION: ClassVar[dict] = "definition"
    definition: Optional[dict] = None

    TASKS: ClassVar[dict] = "tasks"
    tasks: Optional[dict] = None

    STACK_STREAMS: ClassVar[list] = "stack_streams"
    stack_streams: Optional[list] = None

    ASSIGNEES: ClassVar[dict] = "assignees"
    assignees: Optional[dict] = None

    ASSIGNED_TO: ClassVar[dict] = "assigned_to"
    assigned_to: Optional[dict] = None


    def set_definition(self, data):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.DEFINITION).attribute_value(data=data)

    def set_tasks(self, data):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.TASKS).attribute_value(data=data)

    def set_assignees(self, data):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.ASSIGNEES).attribute_value(data=data)

    def set_assigned_to(self, data):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.ASSIGNED_TO).attribute_value(data=data)

    def add_stack_stream(self, data):
        DBAdd(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.STACK_STREAMS).value_to_field(data=data)

    def remove_stack_stream(self, stream_id):
        db_ops = CollectionOperators(db_collection=self.parent_show())
        db_ops.remove_value_from_doc_attr(doc_id=self.id,
                                          attr=self.STACK_STREAMS,
                                          value=stream_id)

    def find_empty_stack_streams(self):
        empty_stacks_ids = []
        get_asset_streams = self.get_stack_streams_documents()

        for stream in get_asset_streams:
            if len(stream["children"]) == 0:
                empty_stacks_ids.append(stream["_id"])
        return empty_stacks_ids

    def get_stack_streams_documents(self):
        stream_documents = []
        db_ops = CollectionOperators(db_collection=self.project_publishes_collection())

        for stream in self.stack_streams:
            streams_doc = db_ops.entity_document(doc_id=stream)
            if streams_doc is not None:
                stream_documents.append(streams_doc)
        return stream_documents


class Project(_EntityBaseModel):
    SHOW_TYPE: ClassVar[str] = "show_type"
    show_type: Optional[str] = None

    SHOW_CODE: ClassVar[str] = "show_code"
    show_code: Optional[str] = None

    SHOW_SETTING: ClassVar[dict] = "show_settings"
    show_settings: Optional[dict] = None

    def set_show_type(self, data: str):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.TYPE).attribute_value(data=data)

    def set_show_code(self, data: str):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.SHOW_CODE).attribute_value(data=data)

    def set_show_settings(self, data: dict):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.id,
              attribute=self.SHOW_SETTING).attribute_value(data=data)


class Projects:
    def names(self):
        delimiter = "__"

        projects_list = []
        get_all_in_database = FindInCollection().all_collections()

        for db_collection in get_all_in_database:
            if delimiter not in db_collection:
                collection_ops = CollectionOperators(db_collection=db_collection)
                get_root_doc = collection_ops.get_root_documents(attrib_field="type", attrib_value="project")
                projects_list.append(get_root_doc[0])


        return projects_list


class WorkFile(_EntityBaseModel):
    DESCRIPTION: ClassVar[str] = "description"
    description: Optional[str] = None

    PARENT_TASK: ClassVar[str] = "parent_task"
    parent_task: Optional[str] = None

    VERSION: ClassVar[str] = "version"
    version: Optional[str] = None

    SESSION_CONTENT: ClassVar[dict] = "session_content"
    session_content: Optional[dict] = None

    REPRESENTATION: ClassVar[dict] = "representation"
    representation: Optional[dict] = None


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


class DBAsset(_EntityBaseModel):
    LABEL: ClassVar[str] = "label"
    label: Optional[str] = None

    MASTER_TASK_TYPE: ClassVar[str] = "task_type"
    master_task_type: Optional[str] = None


class DBAssetVersion(_EntityBaseModel):
    LABEL: ClassVar[str] = "label"
    label: Optional[str] = None

    DB_ASSET_TYPE: ClassVar[str] = "db_asset_type"
    db_asset_type: Optional[str] = None

    DESCRIPTION: ClassVar[str] = "description"
    description: Optional[str] = None

    COMMENTS: ClassVar[list] = "comments"
    comments: Optional[list] = None

    VERSION: ClassVar[str] = "version"
    version: Optional[str] = None

    VERSION_CNT: ClassVar[int] = "version_cnt"
    version_cnt: Optional[int] = None


class DBAssetFileComponent(_EntityBaseModel):
    LABEL: ClassVar[str] = "label"
    label: Optional[str] = None

    FILE_EXTENSION: ClassVar[str] = "file_extension"
    file_extension: Optional[str] = None

    FILE_PATH: ClassVar[str] = "file_path"
    file_path: Optional[str] = None

    VISIBLE: ClassVar[bool] = "visible"
    visible: Optional[bool] = None


class TaskPublish:
    def __init__(self, entity_id=None, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.entity_id = entity_id

    def _create_op_inst(self, attribute_path, value=None):
        method = getattr(self.operation(db_collection=ProjectCollections(connection=Project()).project_publishes_collection(),
                                        entry_id=self.entity_id,
                                        attribute=attribute_path), self.db_operation)

        if value:
            method(value)
        else:
            return method()

    def multiple_ops(self, ops_list):
        for operation_set in ops_list:
            for item_id, operation in operation_set.items():
                for attr_path, attr_value in operation.items():
                    self.entity_id = item_id
                    self._create_op_inst(attribute_path=attr_path, value=attr_value)

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


class CollectionOperators:

    def __init__(self, db_collection=None):
        self.db = MongoConnection().origin_production_database()

        if db_collection is None or len(db_collection) == 0:
            self.collection_name = "empty"
        else:
            self.collection_name = db_collection

        self.db_collection = self.db[self.collection_name]

    def __get_multiple_documents(self, doc_attr=None, **kwargs):
        db_documents = self.db_collection.find(kwargs)
        if len(db_documents) != 0:
            return [doc for doc in db_documents]
        else:
            return db_documents

    def multiple_ops(self, ops: List[Dict[str, Union[str, Any]]]) -> None:
        """
            data format in detail:
               {"entity_id":{"target_attribute":"target_attribute_value"}}

        """

        for operation in ops:
            for entity_id, attribute_target in operation.items():
                target_attribute = list(attribute_target.keys())[0]
                target_attribute_value = list(attribute_target.values())[0]
                DBSet(db_collection=self.collection_name,
                      entry_id=entity_id,
                      attribute=target_attribute).attribute_value(data=target_attribute_value)

    def get_root_documents(self, attrib_field, attrib_value):
        ppe = OriginDBPipelines()
        ppe.add_match_attribute(attribute_field=attrib_field, value_field=attrib_value)

        pipe = ppe.create_pipeline()

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

    def delete_entity_document(self, doc_id):
        self.db_collection.delete_one({"_id": doc_id})

    def remove_value_from_doc_attr(self, doc_id, attr, value):
        self.db_collection.update_one({"_id": doc_id}, {"$pull": {attr: value}})

    def entity_children_ids(self, doc_id):
        db_document = self.db_collection.find_one({"_id": doc_id})
        if db_document:
            return db_document.get(_EntityBaseModel.CHILDREN, [])

    def children_with_parent_id(self, parent_id):
        db_documents = self.db_collection.find({"parent": parent_id})
        return [doc for doc in db_documents]

    def entities_attr_value_starts_with(self, attr_field: str, val_starts_with: str, ids_only=False):
        pipe = OriginDBPipelines()
        pipe.add_attr_value_startswith(attribute_field=attr_field, value_field=val_starts_with)

        pipe.add_sort(sort_by_attr="time", sort_value=-1)
        pipe.add_sort(sort_by_attr="date", sort_value=-1)

        if ids_only:
            pipe.ids_only(only_id=ids_only)

        pipeline = pipe.create_pipeline()

        try:
            if self.db_collection is not None:
                results = list(self.db_collection.aggregate(pipeline))
                return results

        except Exception as e:
            print(__file__, e)

    def get_latest_version_cnt(self):
        pipe = OriginDBPipelines()
        pipe.add_attr_value_startswith("_id", "New_State.assets.chr.red_hulk.red_hulk.modeling.main_pub")
        pipe.add_match_attribute("type", "publish")
        pipe.add_match_attribute("owner", "arsithra")
        pipe.add_sort("version_cnt", -1)



    #########################################################
    #                   TO DO                               #
    #########################################################

    def entities_with_statuses(self, status: str, ids_only=False):
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


if __name__ == "__main__":

    projs = Projects()
    xx = projs.names()
    print(xx)


