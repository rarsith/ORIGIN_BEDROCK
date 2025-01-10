from origin.common_utils import dict_utils
from origin.database.entities.actions import Create
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


class DBPublisher:
    def __init__(self, context: ContextHandler):
        self.context_handler = context

    def create_db_asset(self, parent, publish_type):
        create_entity = Create(context=self.context_handler)
        db_asset_id = create_entity.db_asset(parent=parent,
                                             publish_type=publish_type)
        return db_asset_id

    def create_db_asset_version(self, options):
        create_entity = Create(context=self.context_handler)
        db_asset_version_id = create_entity.db_asset_version(parent_id=self.context_handler.db_asset_id,
                                                             status=options["pub_status"],
                                                             comment=options["pub_comment"])
        return db_asset_version_id

    def create_db_file_components(self,
                                  db_asset_version_id: str,
                                  published_data: dict,
                                  component_parent_id: str) -> None:
        """

        Args:
            db_asset_version_id: specify the id of the db_asset_version that will
            become the parent of the file component created

            published_data: input, dictionary type, format {"fileComponentSlotName": "path/to/saved/data"}

            component_parent_id: optional, the resulting file component db document id can be added to
            the parent (db_asset_version) components field

        Returns: None

        """

        create_entity = Create(context=self.context_handler)
        path_handler = OriginOSPathHandler(context=self.context_handler)
        for file_component_type, file_path in published_data.items():
            unix_file_path = path_handler.resolve_to_relative(file_path, as_unix=True)
            create_entity.db_asset_file_component(visibility=True,
                                                  file_ext=file_component_type,
                                                  file_path=str(unix_file_path),
                                                  parent_id=db_asset_version_id,
                                                  component_parent_id=component_parent_id)

    def create_asset_breakdown_version(self, options):
        curr_breakdown_ver_doc = self.context_handler.database_handler().get_asset_breakdown_latest_version()

        asset_stream_id = self.context_handler.db_asset_stream_id
        asset_stream = asset_stream_id.replace(".", "__") if "." in asset_stream_id else asset_stream_id
        stream_name = asset_stream.rsplit("__", 1)[1]

        asset_breakdown = {asset_stream: {"db_assets": {options["publish_type"]: self.context_handler.db_asset_id}}}

        needs_update = False
        if curr_breakdown_ver_doc is not None:
            current_breakdown = curr_breakdown_ver_doc.data
            if current_breakdown is not None:
                needs_update = dict_utils.is_subset_dict(asset_breakdown, curr_breakdown_ver_doc.data)
                if needs_update:
                    merged_config = dict_utils.merge_dicts(asset_breakdown, curr_breakdown_ver_doc.data)
                    new_db_breakdown_version_id = Create(context=self.context_handler).asset_breakdown_version(
                        data=merged_config)
                    self.context_handler.asset_breakdown_version_id = new_db_breakdown_version_id

                else:
                    self.context_handler.asset_breakdown_version_id = curr_breakdown_ver_doc.id

        else:
            db_breakdown_version_id = Create(context=self.context_handler).asset_breakdown_version(data=asset_breakdown)
            self.context_handler.asset_breakdown_version_id = db_breakdown_version_id

    def create_stack_version(self, options=None):
        Create(context=self.context_handler).asset_stack_version(status="PENDING REVIEW")
