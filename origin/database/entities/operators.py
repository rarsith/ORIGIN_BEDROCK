from typing import List, Tuple

from origin.database.collections.connections import ProjectCollections

from pydantic import BaseModel, Field
from typing import Optional, ClassVar
from origin.database.mongo import DBSet, DBAdd, CollectionOperators, FindInCollection, DBRemove
from origin.common_utils import version_increment as vup


def get_entity_class(item_type):
    if item_type == "group":
        return Group
    if item_type == "asset":
        return Asset
    if item_type == "project":
        return Project
    if item_type == "task":
        return Task


def get_file_component_class(component_type):
    components_file_types = {
        "origin_scene": OriginComponent,
        "origin_meta": OrigiMetaComponent,
        "abc": AlembicArchiveComponent,
        "exr_seq": ImageSequenceComponent,
        "json": JsonComponent,
        "ma": SingleFileAssetComponent,
        "mb": SingleFileAssetComponent,
        "obj": ObjFileComponent,
        "master": OriginComponent,
        "metadata": OrigiMetaComponent,
        "mp4": QuicktimeComponent,
        "mov": QuicktimeComponent,
        "gfr": RenderScriptComponent,
        "gfr_template": RenderScriptComponent,
        "usd": USDComponent,
        "uvs": USDComponent,
        "thumbnail": ThumbnailComponent,
        "wav": AudioComponent,
        "texture": SourceTextureComponent,
        "jpg_seq": JPGImageSequenceComponent,
    }
    return components_file_types.get(component_type)


def get_db_asset_class(publish_type):
    pub_types = {
        "asset_stack_breakdown": AssetStackBreakdown,  # ORIGIN proc
        "asset_stack": AssetStack,  # ORIGIN proc
        "fx_cache": FxCache,  # Houdini Integration Required
        "scene": SceneFile,  # all DDCs Integration Required
        "hda": HoudiniDigitalAsset,  # Houdini Integration Required
        "editorial": EditorialMedia,   # Editing DCC Integration Required - Unknown
        "render": Render,   # Gaffer/Arnold/Cycles Integration Required
        "groom": Groom,  # Houdini Integration Required
        "comp": Comp,  # Natron/Nuke Integration Required
        "look": Look,   # Gaffer/Arnold/Cycles Integration Required
        "template": Template,  # Nuke/Natron/Gaffer/Maya/EditingDCC Integration Required
        "geometry": Geometry,  # Maya/Zbrush
        "usd_assembly": USDAssembly,  # Maya/Houdini/Blender
        "img_seq": ImageSequence,  # Natron/Nuke/Standalone
        "camera": Camera,  # Maya/3DE/Blender/Houdini
        "turntable_camera": TurntableCamera,  # Maya/3DE/Blender/Houdini
        "rig_module": RigModule,  # Maya/
        "animation_rig": AnimationRig,  # Maya
        "texture_set": TextureSet,  # ORIGIN proc
        "texture": Texture,  # Mari/Blender/ZB/Standalone
        "shot_sculpt": ShotSculpt,  # Maya/Blender
        "shot_stack": ShotStack,  # ORIGIN proc
        "shot_breakdown": ShotBreakdown,  # ORIGIN proc
        "animation": Animation,  # Maya/Blender
        "image": Image,  # Natron/Nuke/Gaffer
        "reference": Reference,  # Natron/Nuke/Maya
        "quicktime": Quicktime,  # Natron/Nuke/Maya

    }
    return pub_types.get(publish_type)


class OriginSettingsBase(BaseModel):
    ROOT_PATH: ClassVar[str] = "root_path"
    root_path: Optional[str] = None

    ROOT_ORIGIN_PROJECTS: ClassVar[bool] = "root_origin_projects"
    root_origin_projects: Optional[bool] = None

    APPLICATIONS_REPOSITORY: ClassVar[str] = "applications_repository"
    applications_repository: Optional[str] = None

    MONGODB_CONNECTION_URL: ClassVar[str] = "mongodb_connection_url"
    mongodb_connection_url: Optional[str] = None

    STUDIO_NAME: ClassVar[str] = "studio_name"
    studio_name: Optional[str] = None

    STUDIO_LOGO: ClassVar[str] = "studio_logo"
    studio_logo: Optional[str] = None

    LAST_SESSION: ClassVar[dict] = "last_session"
    last_session: Optional[dict] = None

    DATE: ClassVar[str] = "date"
    date: Optional[str] = None

    TIME: ClassVar[str] = "time"
    time: Optional[str] = None

    OWNER: ClassVar[str] = "owner"
    owner: Optional[str] = None


class OriginSettingsOperations:
    def __init__(self, entity: OriginSettingsBase):
        self.entity = entity

    def set_root_path(self, root_path):
        DBSet(db_collection="Origin",
              entry_id=self.entity.id,
              attribute=self.entity.ROOT_PATH).attribute_value(data=root_path)

    def set_root_origin_projects_path(self, projects_path):
        DBSet(db_collection="Origin",
              entry_id=self.entity.id,
              attribute=self.entity.ROOT_ORIGIN_PROJECTS).attribute_value(data=projects_path)

    def set_applications_repository(self, applications_path):
        DBSet(db_collection="Origin",
              entry_id=self.entity.id,
              attribute=self.entity.APPLICATIONS_REPOSITORY).attribute_value(data=applications_path)

    def set_mongodb_connection(self, mongodb_url):
        DBSet(db_collection="Origin",
              entry_id=self.entity.id,
              attribute=self.entity.MONGODB_CONNECTION_URL).attribute_value(data=mongodb_url)

    def set_studio_name(self, studio_name):
        DBSet(db_collection="Origin",
              entry_id=self.entity.id,
              attribute=self.entity.STUDIO_NAME).attribute_value(data=studio_name)

    def set_studio_logo_path(self, logo_path):
        DBSet(db_collection="Origin",
              entry_id=self.entity.id,
              attribute=self.entity.STUDIO_LOGO).attribute_value(data=logo_path)

    def set_last_session(self, last_session_data):
        DBSet(db_collection="Origin",
              entry_id=self.entity.id,
              attribute=self.entity.LAST_SESSION).attribute_value(data=last_session_data)


class DCCBaseModel(BaseModel):
    ID: ClassVar[str] = "_id"
    id: Optional[str] = Field(None, alias='_id')

    NAME: ClassVar[str] = "name"
    name: Optional[str] = None

    ACTIVE: ClassVar[bool] = "active"
    active: Optional[bool] = None

    TYPE: ClassVar[str] = "type"
    type: Optional[str] = None

    PARENT: ClassVar[str] = "parent"
    parent: Optional[str] = None

    VERSIONS: ClassVar[dict] = "versions"
    versions: Optional[dict] = None

    ICON_PATH: ClassVar[str] = "icon_path"
    icon_path: Optional[str] = None

    DATE: ClassVar[str] = "date"
    date: Optional[str] = None

    TIME: ClassVar[str] = "time"
    time: Optional[str] = None

    OWNER: ClassVar[str] = "owner"
    owner: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }

    def operations(self):
        return EntityOperations(entity=self)


class DCCOperations:
    def __init__(self, entity: DCCBaseModel):
        self.entity = entity

    def add_child(self, db_collection, child_id):
        DBAdd(db_collection=db_collection,
              entry_id=self.entity.id,
              attribute=self.entity.CHILDREN).value_to_field(data=child_id)

    def get_children(self):
        children = []
        doc_data = CollectionOperators(db_collection=self.parent_show())
        children_docs = doc_data.children_with_parent_id(parent_id=self.entity.id)
        for child in children_docs:
            children.append(child)
        return children


class DCCVersion(BaseModel):
    ACTIVE: ClassVar[bool] = "active"
    active: Optional[bool] = None

    VERSION: ClassVar[str] = "version"
    version: Optional[str] = None

    EXEC_PATH: ClassVar[str] = "exec_path"
    exec_path: Optional[str] = None

    # ACTIVE_PLUGINS: ClassVar[dict] = "active_plugins"
    # active_plugins: Optional[dict] = None

    EXEC_PYTHON: ClassVar[str] = "exec_python"
    exec_python: Optional[str] = None

    ENVARS: ClassVar[str] = "envars"
    envars: Optional[str] = None


class DCCVersionOperations:
    def __init__(self, entity: DCCVersion):
        super(DCCVersionOperations, self).__init__(entity=entity)
        self.entity = entity

    def set_parent(self, parent):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.PARENT).attribute_value(data=parent)

    def get_parent(self):
        parent_id = self.entity.id.rsplit(".", 1)[0]
        doc_data = CollectionOperators(db_collection=self.parent_show())
        db_doc = doc_data.entity_document(doc_id=parent_id)
        return DCCVersion(**db_doc)


class PublishOptions(BaseModel):
    PARENT_DB_ASSET_ID: ClassVar[str] = "parent_db_asset_id"
    parent_db_asset_id: Optional[str] = None

    PARENT_DB_ASSET_TYPE: ClassVar[str] = "parent_db_asset_type"
    parent_db_asset_type: Optional[str] = None

    PERSISTENT_FILE_FORMATS: ClassVar[str] = "persistent_file_formats"
    persistent_file_formats: Optional[str] = None

    QUALITY_CHECKS: ClassVar[str] = "quality_checks"
    quality_checks: Optional[str] = None

    OPTIONAL_FILE_FORMATS: ClassVar[list] = "optional_file_formats"
    optional_file_formats: Optional[list] = None

    COLLECTIONS: ClassVar[dict] = "collections"
    collections: Optional[dict] = None

    REVIEW_OPTIONS: ClassVar[list] = "review_options"
    review_options: Optional[list] = None

    ADDITIONAL_OPERATIONS: ClassVar[list] = "additional_operations"
    additional_operations: Optional[list] = None

    STACK_STREAM_ID: ClassVar[str] = "stack_stream_id"
    stack_stream_id: Optional[str] = None

    PUBLISH_COMMENT_ID: ClassVar[str] = "publish_comment_id"
    publish_comment_id: Optional[str] = None

    PUBLISH_STATUS: ClassVar[str] = "publish_status"
    publish_status: Optional[str] = None

    PUBLISH_TYPE: ClassVar[str] = "publish_type"
    publish_type: Optional[str] = None


class EntityBaseModel(BaseModel):
    ID: ClassVar[str] = "_id"
    id: Optional[str] = Field(None, alias='_id')

    NAME: ClassVar[str] = "name"
    name: Optional[str] = None

    ACTIVE: ClassVar[bool] = "active"
    active: Optional[bool] = None

    TYPE: ClassVar[str] = "type"
    type: Optional[str] = None

    PARENT: ClassVar[str] = "parent"
    parent: Optional[str] = None

    BREAKDOWN: ClassVar[str] = "breakdown"
    breakdown: Optional[str] = None

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



    model_config = {
        "from_attributes": True,
    }

    def operations(self):
        return EntityOperations(entity=self)


class EntityOperations:
    def __init__(self, entity: EntityBaseModel):
        self.entity = entity

    def parent_show(self):
        delimiter = "."

        if delimiter not in self.entity.id:
            return self.entity.id

        parent_show = self.entity.id.split(delimiter, 1)[0]
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
        parent_id = self.entity.id.rsplit(".", 1)[0]
        doc_data = CollectionOperators(db_collection=self.parent_show())
        db_doc = doc_data.entity_document(doc_id=parent_id)
        return EntityBaseModel(**db_doc)

    def set_parent(self, parent):
        DBSet(db_collection=self.parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.PARENT).attribute_value(data=parent)

    def add_child(self, db_collection, child_id):
        DBAdd(db_collection=db_collection,
              entry_id=self.entity.id,
              attribute=self.entity.CHILDREN).value_to_field(data=child_id)

    def get_children(self):
        children = []
        doc_data = CollectionOperators(db_collection=self.parent_show())
        children_docs = doc_data.children_with_parent_id(parent_id=self.entity.id)
        for child in children_docs:
            children.append(child)
        return children


class Asset(EntityBaseModel):
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

    def operations(self):
        return AssetOperations(entity=self)


class AssetOperations(EntityOperations):
    def __init__(self, entity: Asset):
        super(AssetOperations, self).__init__(entity=entity)
        self.entity = entity

    def set_definition(self, data):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.DEFINITION).attribute_value(data=data)

    def set_tasks(self, data):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.TASKS).attribute_value(data=data)

    def set_assignees(self, data):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.ASSIGNEES).attribute_value(data=data)

    def set_assigned_to(self, data):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.ASSIGNED_TO).attribute_value(data=data)

    def add_stack_stream(self, data):
        DBAdd(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.STACK_STREAMS).value_to_field(data=data)

    def remove_stack_stream(self, stream_id):
        db_ops = CollectionOperators(db_collection=self.entity.operations().parent_show())
        db_ops.remove_value_from_doc_attr(doc_id=self.entity.id,
                                          attr=self.entity.STACK_STREAMS,
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
        db_ops = CollectionOperators(db_collection=self.entity.operations().project_publishes_collection())

        for stream in self.entity.stack_streams:
            streams_doc = db_ops.entity_document(doc_id=stream)
            if streams_doc is not None:
                stream_documents.append(streams_doc)
        return stream_documents

    def set_asset_breakdown(self, breakdown_id):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.BREAKDOWN).attribute_value(data=breakdown_id)

    def get_asset_breakdown(self):
        db_ops = CollectionOperators(db_collection=self.entity.operations().project_publishes_collection())

        if self.entity.breakdown is not None:
            breakdown_doc_data = db_ops.entity_document(doc_id=self.entity.breakdown)
            breakdown_doc = AssetBreakdown(**breakdown_doc_data)
            latest_version_doc_data = breakdown_doc.operations().get_latest_version()

            return AssetBreakdownVersion(**latest_version_doc_data)


class Group(EntityBaseModel):
    DATA: ClassVar[dict] = "data"
    data: Optional[dict] = None


class Project(EntityBaseModel):
    SHOW_TYPE: ClassVar[str] = "show_type"
    show_type: Optional[str] = None

    SHOW_CODE: ClassVar[str] = "show_code"
    show_code: Optional[str] = None

    SHOW_SETTING: ClassVar[dict] = "show_settings"
    show_settings: Optional[dict] = None

    SHOW_SITE: ClassVar[dict] = "show_site"
    show_site: Optional[dict] = None

    def operations(self):
        return ProjectOperations(entity=self)


class ProjectOperations(EntityOperations):
    def __init__(self, entity: Project):
        super(ProjectOperations, self).__init__(entity=entity)
        self.entity = entity

    def set_show_type(self, data: str):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.TYPE).attribute_value(data=data)

    def set_show_code(self, data: str):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.SHOW_CODE).attribute_value(data=data)

    def set_show_settings(self, data: dict):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.SHOW_SETTING).attribute_value(data=data)


class Task(EntityBaseModel):
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

    def operations(self):
        return TaskOperations(entity=self)


class TaskOperations(EntityOperations):
    def __init__(self, entity: Task):
        super(TaskOperations, self).__init__(entity=entity)
        self.entity = entity

    def set_artist(self, data: str):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.ARTIST).attribute_value(data=data)

    def add_imports_from(self, data: dict):
        DBAdd(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.IMPORTS_FROM).value_to_field(data=data)

    def set_bid_days(self, data: str):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.BID_DAYS).attribute_value(data=data)

    def set_end_date(self, data: str):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.END_DATE).attribute_value(data=data)

    def add_milestones(self, data: dict):
        DBAdd(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.MILESTONES).value_to_field(data=data)

    def set_start_date(self, data: str):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.START_DATE).attribute_value(data=data)

    def set_worked_days(self, data: str):
        DBSet(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.WORKED_DAYS).attribute_value(data=data)

    def add_previous_artists(self, data: str):
        DBAdd(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.PREVIOUS_ARTISTS).value_to_field(data=data)


class WorkFile(EntityBaseModel):
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

    def operations(self):
        return WorkFileOperators(entity=self)


class WorkFileOperators(EntityOperations):
    def __init__(self, entity: WorkFile):
        super(WorkFileOperators, self).__init__(entity=entity)
        self.entity = entity

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


class DBAsset(EntityBaseModel):
    LABEL: ClassVar[str] = "label"
    label: Optional[str] = None

    STACKS: ClassVar[list] = "stacks"
    stacks: Optional[list] = None

    MASTER_TASK_TYPE: ClassVar[str] = "task_type"
    master_task_type: Optional[str] = None

    VERSION_CNT: ClassVar[int] = "version_cnt"
    version_cnt: Optional[int] = 0

    DB_ASSET_TYPE: ClassVar[str] = "db_asset_type"
    db_asset_type: Optional[str] = None

    def operations(self):
        return DBAssetOperations(entity=self)


class DBAssetOperations(EntityOperations):
    def __init__(self, entity: DBAsset):
        super(DBAssetOperations, self).__init__(entity=entity)
        self.entity = entity

    def update_version_count(self, increment: int):
        next_version = self.entity.version_cnt + increment
        DBSet(db_collection=self.entity.operations().project_publishes_collection(),
              entry_id=self.entity.id,
              attribute=self.entity.VERSION_CNT).attribute_value(data=next_version)

    def get_all_versions(self) -> List[dict]:
        data_ops = CollectionOperators(db_collection=self.entity.operations().project_publishes_collection())
        all_versions = data_ops.entities_attr_value_starts_with(attr_field="_id",
                                                                val_starts_with=self.entity.id,
                                                                extra_filters=[{self.entity.TYPE: "publish"}])
        return all_versions

    def get_latest_version(self, db_asset_type=None, with_status=None):
        if self.entity.version_cnt != 0:
            resolve_db_asset_version = f'v{self.entity.version_cnt:04}'
            db_asset_version_id = ".".join([self.entity.id, resolve_db_asset_version])
            data_ops = CollectionOperators(db_collection=self.entity.operations().project_publishes_collection())

            if with_status is not None:
                latest_version_doc_data = data_ops.get_all_versions_with_status(db_asset=self.entity,
                                                                                db_asset_type=db_asset_type,
                                                                                status=with_status,
                                                                                ids_only=True)
                return latest_version_doc_data
            else:
                latest_version_doc_data = data_ops.entity_document(doc_id=db_asset_version_id)
                return latest_version_doc_data
        else:
            return None

    def get_next_version(self):
        version_string, version = vup.version_up(self.entity.version_cnt)
        return version_string, version

    def add_stack(self, db_collection, stack_id):
        DBAdd(db_collection=db_collection,
              entry_id=self.entity.id,
              attribute=self.entity.STACKS).value_to_field(data=stack_id)


class AssetBreakdown(DBAsset):
    type: Optional[str] = "db_asset_breakdown"
    db_asset_type: Optional[str] = "db_asset_breakdown"


class StackSlot(EntityBaseModel):
    SLOT: ClassVar[dict] = "slot"
    slot: Optional[dict] = None


class StackBaseModel(DBAsset):
    SLOTS: ClassVar[dict] = "slots"
    slots: Optional[dict] = None

    OPTIONS: ClassVar[dict] = "options"
    options: Optional[dict] = None

    ORIGIN_DATA: ClassVar[dict] = "origin_data"
    origin_data: Optional[dict] = None

    def operations(self):
        return StackOperations(entity=self)


class StackOperations(DBAssetOperations):
    def __init__(self, entity: StackBaseModel):
        super(StackOperations, self).__init__(entity=entity)
        self.entity = entity

    def add_slot(self, db_asset_id):
        DBAdd(db_collection=self.entity.operations().parent_show(),
              entry_id=self.entity.id,
              attribute=self.entity.SLOTS).value_to_field(data=db_asset_id)


class AssetStackBreakdown(StackBaseModel):
    type: Optional[str] = "asset_stack_breakdown"


class AssetStack(StackBaseModel):
    type: Optional[str] = "asset_stack"


class ShotStack(StackBaseModel):
    type: Optional[str] = "shot_stack"


class ShotBreakdown(StackBaseModel):
    type: Optional[str] = "shot_stack_breakdown"


class FxCache(DBAsset):
    type: Optional[str] = "fx_cache"


class SceneFile(DBAsset):
    type: Optional[str] = "scene"


class HoudiniDigitalAsset(DBAsset):
    type: Optional[str] = "hda"


class EditorialMedia(DBAsset):
    type: Optional[str] = "editorial"


class Render(DBAsset):
    type: Optional[str] = "render"


class Groom(DBAsset):
    type: Optional[str] = "groom"


class Comp(DBAsset):
    type: Optional[str] = "comp"


class Look(DBAsset):
    type: Optional[str] = "look"


class Template(DBAsset):
    type: Optional[str] = "template"


class Geometry(DBAsset):
    type: Optional[str] = "geometry"


class USDAssembly(DBAsset):
    type: Optional[str] = "usd_assembly"


class ImageSequence(DBAsset):
    type: Optional[str] = "img_seq"


class Camera(DBAsset):
    type: Optional[str] = "camera"


class TurntableCamera(DBAsset):
    type: Optional[str] = "turntable_camera"


class RigModule(DBAsset):
    type: Optional[str] = "rig_module"


class AnimationRig(DBAsset):
    type: Optional[str] = "animation_rig"


class TextureSet(DBAsset):
    type: Optional[str] = "texture_set"


class Texture(DBAsset):
    type: Optional[str] = "texture"


class Animation(DBAsset):
    type: Optional[str] = "animation"


class ShotSculpt(DBAsset):
    type: Optional[str] = "shot_sculpt"


class Image(DBAsset):
    type: Optional[str] = "image"


class Reference(DBAsset):
    type: Optional[str] = "reference"


class Quicktime(DBAsset):
    type: Optional[str] = "quicktime"


class DBAssetVersion(EntityBaseModel):
    LABEL: ClassVar[str] = "label"
    label: Optional[str] = None

    DB_ASSET_TYPE: ClassVar[str] = "db_asset_type"
    db_asset_type: Optional[str] = None

    PARENT_TASK_TYPE: ClassVar[str] = "parent_task_type"
    parent_task_type: Optional[str] = None

    PARENT_TASK_ID: ClassVar[str] = "parent_task_id"
    parent_task_id: Optional[str] = None

    DESCRIPTION: ClassVar[str] = "description"
    description: Optional[str] = None

    COMMENTS: ClassVar[list] = "comments"
    comments: Optional[list] = None

    VERSION: ClassVar[str] = "version"
    version: Optional[str] = None

    VERSION_CNT: ClassVar[int] = "version_cnt"
    version_cnt: Optional[int] = None

    COMPONENTS: ClassVar[list] = "components"
    components: Optional[list] = None

    ORIGIN_DATA: ClassVar[dict] = "origin_data"
    origin_data: Optional[dict] = None


class AssetBreakdownVersion(DBAssetVersion):
    db_asset_type: Optional[str] = "db_asset_breakdown_version"

    DATA: ClassVar[dict] = "data"
    data: Optional[dict] = None

    def operations(self):
        return AssetBreakdownVersionOperations(entity=self)


class AssetBreakdownVersionOperations(DBAssetOperations):
    def __init__(self, entity: AssetBreakdown):
        super(AssetBreakdownVersionOperations, self).__init__(entity=entity)
        self.entity = entity

    def add_data(self, db_asset_stream_doc: DBAsset, db_asset_doc: DBAsset):
        """

        Args:
            db_asset_stream_doc: instance of the DBAsset
            db_asset_doc: instance of DBAsset
            data: instance of DBAsset

        Returns:

        """
        data_path = ".".join([self.entity.DATA, db_asset_stream_doc.id, db_asset_doc.stack_slot])

        DBSet(db_collection=self.entity.operations().project_publishes_collection(),
              entry_id=self.entity.id,
              attribute=data_path).attribute_value(data=db_asset_doc.id)

    def remove_data(self, db_asset_stream_doc: DBAsset, db_asset_doc: DBAsset):
        """

                Args:
                    db_asset_stream_doc: instance of the DBAsset
                    db_asset_doc: instance of DBAsset
                    data: instance of DBAsset

                Returns:

                """
        data_path = ".".join([self.entity.DATA, db_asset_stream_doc.id, db_asset_doc.stack_slot])

        DBRemove(db_collection=self.entity.operations().project_publishes_collection(),
                 entry_id=self.entity.id,
                 attribute=data_path).attribute_value(data=db_asset_doc.id)


class AssetStackVersion(DBAssetVersion):
    db_asset_type: Optional[str] = "db_asset__stack_version"

    DATA: ClassVar[dict] = "data"
    data: Optional[dict] = None

    def operations(self):
        return AssetStackVersionOperations(entity=self)


class AssetStackVersionOperations(DBAssetOperations):
    def __init__(self, entity: AssetBreakdown):
        super(AssetStackVersionOperations, self).__init__(entity=entity)
        self.entity = entity


class DBAssetFileComponent(EntityBaseModel):
    LABEL: ClassVar[str] = "label"
    label: Optional[str] = None

    FILE_EXTENSION: ClassVar[str] = "file_extension"
    file_extension: Optional[str] = None

    FILE_PATH: ClassVar[str] = "file_path"
    file_path: Optional[str] = None

    VISIBLE: ClassVar[bool] = "visible"
    visible: Optional[bool] = None

    DB_ASSET_TYPE: ClassVar[str] = "db_asset_type"
    db_asset_type: Optional[str] = None


class AlembicArchiveComponent(DBAssetFileComponent):
    type: Optional[str] = "alembic_component"
    label: Optional[str] = "alembic"
    file_extension: Optional[str] = "abc"


class ImageSequenceComponent(DBAssetFileComponent):
    type: Optional[str] = "image_sequence_component"
    label: Optional[str] = "image_sequence"
    file_extension: Optional[str] = "exr"


class JsonComponent(DBAssetFileComponent):
    type: Optional[str] = "json_component"
    label: Optional[str] = "json"
    file_extension: Optional[str] = "json"


class MayaSceneComponent(DBAssetFileComponent):
    type: Optional[str] = "maya_scene_component"
    label: Optional[str] = "maya_scene"
    file_extension: Optional[str] = "ma"


class ObjFileComponent(DBAssetFileComponent):
    type: Optional[str] = "obj_component"
    label: Optional[str] = "obj"
    file_extension: Optional[str] = "obj"


class OriginComponent(DBAssetFileComponent):
    type: Optional[str] = "origin_scene_component"
    label: Optional[str] = "origin_scene"


class OrigiMetaComponent(DBAssetFileComponent):
    type: Optional[str] = "origin_meta_component"
    label: Optional[str] = "origin_meta"
    file_extension: Optional[str] = "origin_meta"


class QuicktimeComponent(DBAssetFileComponent):
    type: Optional[str] = "review_component"
    label: Optional[str] = "review"
    file_extension: Optional[str] = "mov"


class RenderScriptComponent(DBAssetFileComponent):
    type: Optional[str] = "render_script_component"
    label: Optional[str] = "render_script"
    file_extension: Optional[str] = "gfr"


class RenderScriptTemplateComponent(DBAssetFileComponent):
    type: Optional[str] = "render_template_component"
    label: Optional[str] = "render_template"
    file_extension: Optional[str] = "gfr"


class SingleFileAssetComponent(DBAssetFileComponent):
    pass


class USDComponent(DBAssetFileComponent):
    type: Optional[str] = "USD_component"
    label: Optional[str] = "USD"
    file_extension: Optional[str] = "usd"


class ModelingUVSnapShotComponent(DBAssetFileComponent):
    type: Optional[str] = "UV_component"
    label: Optional[str] = "UV"

    UDIM_TILES: ClassVar[List[int]] = "udim_tiles"
    udim_tiles: Optional[List[int]] = None

    UV_TILES: ClassVar[List[Tuple[int, int]]] = "uv_tiles"
    uv_tiles: Optional[List[Tuple[int, int]]] = None


class ThumbnailComponent(DBAssetFileComponent):
    type: Optional[str] = "thumbnail_component"
    label: Optional[str] = "thumbnail"
    file_extension: Optional[str] = "png"


class AudioComponent(DBAssetFileComponent):
    type: Optional[str] = "audio_component"
    label: Optional[str] = "audio"
    file_extension: Optional[str] = "wav"


class SourceTextureComponent(DBAssetFileComponent):
    type: Optional[str] = "source_texture_component"
    label: Optional[str] = "source_texture"
    file_extension: Optional[str] = "exr"


class JPGImageSequenceComponent(DBAssetFileComponent):
    type: Optional[str] = "jpg__img_seq__component"
    label: Optional[str] = "source_jpg"
    file_extension: Optional[str] = "jpg"


class TaskPublish:
    def __init__(self, entity_id=None, operation=None, db_operation=None):
        self.operation = operation
        self.db_operation = db_operation
        self.entity_id = entity_id

    def _create_op_inst(self, attribute_path, value=None):
        method = getattr(
            self.operation(db_collection=ProjectCollections(connection=Project()).project_publishes_collection(),
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


if __name__ == "__main__":
    projs = Projects()
    xx = projs.names()
    # print(xx)
