from typing import Optional
from pydantic import BaseModel
from origin.envars import ContextHandler
from common_utils.date_time import DateTime
from common_utils.users import Users


class DBAssetConstruct(BaseModel):
    label: Optional[str]
    entry_name: Optional[str]
    show_name: Optional[str]
    task_type: Optional[str]
    server_path: Optional[str]
    origin_db_path: Optional[str]
    type: Optional[str]
    versions: Optional[list]
    parent: Optional[str]
    children: Optional[list]
    date: Optional[str]
    time: Optional[str]
    owner: Optional[str]


class DbAsset:

    def __init__(self, context: ContextHandler):

        self.db_asset_construct = DBAssetConstruct()
        self.context = context

    def create(self, name):
        self.db_asset_construct.label = self.__resolve_label()
        self.db_asset_construct.entry_name = name
        self.db_asset_construct.show_name = self.context["show_name"]
        self.db_asset_construct.task_type = self.context["task_type"]
        self.db_asset_construct.server_path = self.__resolve_server_path()
        self.db_asset_construct.origin_db_path = self.__resolve_origin_db_path()
        self.db_asset_construct.type = self.__resolve_db_asset_type()
        self.db_asset_construct.parent = self.__resolve_parent()
        self.db_asset_construct.children = []
        self.db_asset_construct.date = DateTime().curr_date()
        self.db_asset_construct.time = DateTime().curr_time()
        self.db_asset_construct.owner = Users().curr_user()

        insert_document = self.db_asset_construct.__dict__

    def get_task_db_assets(self):
        pass

    def get_versions(self, db_asset_id):
        pass

    def append_version(self, version_id):
        pass

    def get_latest_version(self, db_asset_id):
        pass

    def get_versions_with_status(self, db_asset_id, status):
        pass

    def __resolve_label(self):
        return

    def __resolve_server_path(self):
        pass

    def __resolve_origin_db_path(self):
        pass

    def __resolve_db_asset_type(self):
        pass

    def __resolve_parent(self):
        pass


class DBAssetVersion:
    pass

# class DBAssetVersion(DBAsset):
#     components: Optional[list]

class AssetBreakdown:
    pass


class AssetStack:
    pass


class FxCache:
    pass


class SceneFile:
    pass


class HoudiniDigitalAsset:
    pass


class EditorialMedia:
    pass


class Render:
    pass


class Groom:
    pass


class Comp:
    pass


class Look:
    pass


class Template:
    pass


class Geometry:
    pass


class ImageSequence:
    pass


class Camera:
    pass


class RigModule:
    pass


class AnimationRig:
    pass


class TexturePackage:
    pass


class Texture:
    pass


class ShotStack:
    pass


class ShotBreakdown:
    pass


class Animation:
    pass


class Image:
    pass


class Reference:
    pass
