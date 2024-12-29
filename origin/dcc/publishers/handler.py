from pydantic import BaseModel
from typing import ClassVar, Optional

from origin.envars.origin_envars import ContextHandler


class PublishOptions(BaseModel):
    CONTEXT_OBJECT: ClassVar[str] = "context_object"
    context_object: Optional[ContextHandler] = None

    PARENT_DB_ASSET_ID: ClassVar[str] = "parent_db_asset_id"
    parent_db_asset_id: Optional[str] = ''

    PARENT_DB_ASSET_TYPE: ClassVar[str] = "parent_db_asset_type"
    parent_db_asset_type: Optional[str] = ''

    PERSISTENT_FILE_FORMATS: ClassVar[str] = "persistent_file_formats"
    persistent_file_formats: Optional[str] = ''

    QUALITY_CHECKS: ClassVar[str] = "quality_checks"
    quality_checks: Optional[str] = ''

    OPTIONAL_FILE_FORMATS: ClassVar[list] = "optional_file_formats"
    optional_file_formats: Optional[list] = []

    COLLECTIONS: ClassVar[dict] = "collections"
    collections: Optional[dict] = {}

    REVIEW_MEDIUM: ClassVar[list] = "review_medium"
    review_medium: Optional[list] = []

    REVIEW_OPTIONS: ClassVar[list] = "review_options"
    review_options: Optional[list] = []

    ADDITIONAL_PUBLISHES: ClassVar[list] = "additional_publishes"
    additional_publishes: Optional[list] = []

    STACK_STREAM_ID: ClassVar[str] = "stack_stream_id"
    stack_stream_id: Optional[str] = ''

    PUBLISH_COMMENT_ID: ClassVar[str] = "publish_comment_id"
    publish_comment_id: Optional[str] = ''

    PUBLISH_STATUS: ClassVar[str] = "publish_status"
    publish_status: Optional[str] = ''

    PUBLISH_TYPE: ClassVar[str] = "publish_type"
    publish_type: Optional[str] = ''

    STACK_UPDATE: ClassVar[bool] = "stack_update"
    stack_update: Optional[bool] = False

