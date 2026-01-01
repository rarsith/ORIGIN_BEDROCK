from origin.common_utils import dict_utils
from origin.database.entities.actions import Create
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


class DBPublisher:
    def __init__(self, options=None):

        self.context_handler = ContextHandler()

        if options is not None:
            self.options = options

            if isinstance(self.options["context_object"], dict):
                self.context_handler.load_session(self.options["context_object"])
            else:
                self.context_handler = self.options["context_object"]

    def create_db_asset(self, context, parent, publish_type):
        create_entity = Create(context=context)
        db_asset_id = create_entity.db_asset(parent=parent,
                                             publish_type=publish_type)
        return db_asset_id

    def create_db_asset_version(self, context, parent_id):
        create_entity = Create(context=context)
        db_asset_version_id = create_entity.db_asset_version(parent_id=parent_id,
                                                             status=self.options["pub_status"],
                                                             comment=self.options["pub_comment"])
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

    def create_db_custom_file_components(self,
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
            create_entity.db_asset_custom_file_component(visibility=True,
                                                         file_ext=file_component_type,
                                                         file_path=str(unix_file_path),
                                                         parent_id=db_asset_version_id,
                                                         component_parent_id=component_parent_id,
                                                         label=file_component_type)

    # def create_asset_breakdown_version(self, context: ContextHandler):
    #     curr_breakdown_ver_doc = context.database_handler().get_asset_breakdown_latest_version()
    #
    #     asset_stream_id = context.db_asset_stream_id
    #     asset_stream = asset_stream_id.replace(".", "__") if "." in asset_stream_id else asset_stream_id
    #     stream_name = asset_stream.rsplit("__", 1)[1]
    #
    #     asset_breakdown = {asset_stream: {"db_assets": {self.options["publish_type"]: context.db_asset_id}}}
    #
    #     needs_update = False
    #     if curr_breakdown_ver_doc is not None:
    #         current_breakdown = curr_breakdown_ver_doc.data
    #         if current_breakdown is not None:
    #             needs_update = dict_utils.is_subset_dict(asset_breakdown, curr_breakdown_ver_doc.data)
    #             if needs_update:
    #                 merged_config = dict_utils.merge_dicts(asset_breakdown, curr_breakdown_ver_doc.data)
    #                 Create(context=context).asset_breakdown_version(
    #                     data=merged_config)
    #
    #     else:
    #         db_breakdown_version_id = Create(context=context).asset_breakdown_version(data=asset_breakdown)
    #         context.asset_breakdown_version_id = db_breakdown_version_id

    def create_asset_breakdown_version(self, context: ContextHandler):
        curr_breakdown_ver_doc = context.database_handler().get_asset_breakdown_latest_version()

        asset_breakdown = {"db_assets": {self.options["publish_type"]: context.db_asset_id}}

        needs_update = False
        if curr_breakdown_ver_doc is not None:
            current_breakdown = curr_breakdown_ver_doc.data
            if current_breakdown is not None:
                needs_update = dict_utils.is_subset_dict(asset_breakdown, curr_breakdown_ver_doc.data)
                if needs_update:
                    merged_config = dict_utils.merge_dicts(asset_breakdown, curr_breakdown_ver_doc.data)
                    Create(context=context).asset_breakdown_version(
                        data=merged_config)

        else:
            db_breakdown_version_id = Create(context=context).asset_breakdown_version(data=asset_breakdown)
            context.asset_breakdown_version_id = db_breakdown_version_id


    # def create_stack_version(self, context: ContextHandler):
    #     Create(context=context).asset_stack_version(status="WIP")

    def create_stack_version(self, context: ContextHandler, slots: dict = None):
        if slots is None:
            Create(context=context).asset_stack_version(status="WIP")
        else:
            Create(context=context).asset_stack_version_slots(status="WIP", slots=slots)
