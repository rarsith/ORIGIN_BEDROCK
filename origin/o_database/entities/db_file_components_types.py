from typing import Optional, List, Tuple
from pydantic import BaseModel


class FileComponents(BaseModel):
    origin_id: Optional[str] = None
    origin_db_path: Optional[str] = None
    entry_name: Optional[str] = None
    display_name: Optional[str] = None
    server_path: Optional[str] = None
    version: Optional[str] = None
    version_cnt: Optional[int] = None
    parent: Optional[str] = None
    children: Optional[str] = None
    extension: Optional[List[str]] = None
    reviewable: Optional[bool] = False
    metadata: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    owner: Optional[str] = None


class SingleFileAssetComponent(FileComponents):
    pass


class MayaSceneComponent(FileComponents):
    pass


class AlembicArchiveComponent(FileComponents):
    pass


class ObjFileComponent(FileComponents):
    pass


class ModelingUVSnapShotComponent(FileComponents):
    udim_tiles: Optional[List[int]] = None
    uv_tiles: Optional[List[Tuple[int, int]]] = None


class USDComponent(FileComponents):
    pass


class GafferScriptComponent(FileComponents):
    pass


class ImageSequenceComponent(FileComponents):
    pass


class OriginComponent(FileComponents):
    pass


class OrigiMetaComponent(FileComponents):
    pass


class JsonComponent(FileComponents):
    pass


class QuicktimeComponent(FileComponents):
    pass


class ThumbnailComponent(FileComponents):
    pass


class AudioComponent(FileComponents):
    pass


class SourceTextureComponent(FileComponents):
    pass


if __name__ == "__main__":
    thumb = ModelingUVSnapShotComponent()
    thumb.origin_id = "590384owhefjhg8998w475"
    thumb.display_name = "uv"
    thumb.udim_tiles = [1001, 1002, 1003]
    print(thumb.__dict__)