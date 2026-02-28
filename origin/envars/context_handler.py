from origin.database.entities.operators import Project, Asset, Group, Task, DBAsset, AssetBreakdown, DBAssetVersion, \
    AssetBreakdownVersion, AssetStack, AssetStackVersion
from origin.database.mongo import CollectionOperators
from origin.database.mongo_connection import MongoConnection
from origin.envars.origin_envarsXXX import ContextHandler


class OriginDatabaseHandler:
    def __init__(self, context: ContextHandler):
        self.__context = context

        self.__db = MongoConnection().origin_production_database()
        self.__project_structure_collection = self.__db[self.__context.show_name]
        self.__project_publishes_collection = self.__db[self.__context.project_publishes]
        self.__project_control_collection = self.__db[self.__context.project_control]
        self.__project_work_collection = self.__db[self.__context.project_work]

    def get_db_document_by_id(self, db_collection, doc_id):
        db_ops = CollectionOperators(db_collection=db_collection)
        document = db_ops.entity_document(doc_id=doc_id)
        # document_object = get_entity_class(item_type=document['type'])(**document)
        # print(document_object.type)
        return document

    # def get_db_document_by_id(self, db_collection, doc_id):
    #     db_ops = CollectionOperators(db_collection=db_collection)
    #     document = db_ops.entity_document(doc_id=doc_id)
    #     document_object = get_entity_class(item_type=document['type'])(**document)
    #     return document_object

    # def get_document_by_id(self, doc_id, db_collection: DatabaseConnections):
    #     db_ops = None
    #     if db_collection == DatabaseConnections.project_structure_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.show_name)
    #     elif db_collection == DatabaseConnections.project_publishes_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.project_publishes)
    #     elif db_collection == DatabaseConnections.project_control_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.project_control)
    #     elif db_collection == DatabaseConnections.project_work_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.project_work)
    #
    #     document = db_ops.entity_document(doc_id=doc_id)
    #     return document

    def get_project_document(self) -> Project:
        project_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                                 doc_id=self.__context.show_name)
        return Project(**project_doc)

    def get_asset_document(self) -> Asset:
        entity_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                                doc_id=self.__context.entity_id)

        if self.__context.entity_type == "group":
            return Group(**entity_doc)
        else:
            return Asset(**entity_doc)

    def get_task_document(self) -> Task:
        task_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                              doc_id=self.__context.task_id)
        return Task(**task_doc)

    def get_db_asset_stream_document(self):
        if self.__context.db_asset_stream_id:
            db_asset_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                      doc_id=self.__context.db_asset_stream_id)

            return DBAsset(**db_asset_doc)
        else:
            return None

    def get_db_asset_document(self):
        if self.__context.db_asset_id is not None:
            db_asset_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                      doc_id=self.__context.db_asset_id)

            if db_asset_doc is not None:
                return DBAsset(**db_asset_doc)
            else:
                return None

    def get_stream_breakdown(self):
        if self.__context.asset_breakdown_id:
            breakdown_doc_data = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                            doc_id=self.__context.asset_breakdown_id)
            return AssetBreakdown(**breakdown_doc_data)
        else:
            return None

    def get_db_asset_version_document(self):
        if self.__context.db_asset_version_id is not None:
            db_asset_version_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                              doc_id=self.__context.db_asset_version_id)

            if db_asset_version_doc is not None:
                return DBAssetVersion(**db_asset_version_doc)
            else:
                return None

    def get_asset_streams(self):
        db_ops = CollectionOperators(db_collection=self.__context.show_name)
        entity_doc = db_ops.entity_document(doc_id=self.__context.entity_id)
        if entity_doc is not None:
            asset_doc = Asset(**entity_doc)

            curr_asset_type = self.__context.entity_type
            stack_steams = asset_doc.stack_streams

            if curr_asset_type != "group":
                if stack_steams is None:
                    return {}
                if len(stack_steams) == 0:
                    return {}
                else:
                    return stack_steams

    def get_asset_breakdown_latest_version(self):
        breakdown_doc = self.get_stream_breakdown()
        if breakdown_doc is not None:
            latest_version_doc_data = breakdown_doc.operations().get_latest_version()
            if latest_version_doc_data is not None:
                return AssetBreakdownVersion(**latest_version_doc_data)
            else:
                return None
        else:
            return None

    def get_asset_breakdown_context_slots(self):
        breakdown_latest_version = self.get_asset_breakdown_latest_version()
        if breakdown_latest_version is not None:
            breakdown_data = breakdown_latest_version.data
            asset_stream_id = self.__context.db_asset_stream_id
            clean_asset_stream_id = asset_stream_id.replace(".", "__")
            context_slots = breakdown_data["db_assets"]
            return context_slots
        else:
            return None

    def get_stack_document(self):
        stack_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                               doc_id=self.__context.stack_id)
        if stack_doc is not None:
            return AssetStack(**stack_doc)
        else:
            return None

    def get_stack_latest_version(self, with_status=None):
        stack_doc = self.get_stack_document()
        if stack_doc is not None:
            latest_version_doc_data = stack_doc.operations().get_latest_version(db_asset_type="db_asset__stack_version",
                                                                                with_status=with_status)
            if latest_version_doc_data is not None:
                return AssetStackVersion(**latest_version_doc_data)
            else:
                return None
        else:
            return None

    def collection(self):
        pass  # use of Create Module

    def get_stream_stack(self):
        db_ops = CollectionOperators(db_collection=self.__context.project_publishes)

        if self.__context.db_asset_stream_id is not None:
            stream_stack_db_asset_id = self.__context.db_asset_stream_id + "." + "asset_stack"
            stack_doc = db_ops.entity_document(doc_id=stream_stack_db_asset_id)
            return stack_doc

        else:
            return None

    def get_current_stack_version(self):
        db_ops = CollectionOperators(db_collection=self.__context.project_publishes)
        stack_doc = self.get_stream_stack()

        if stack_doc is not None:
            current_doc = db_ops.get_current_version(_id={"$regex": f"^{stack_doc['_id']}"})
            if len(current_doc) != 0:
                return current_doc[0]
            else:
                return None
        else:
            return None

    def get_current_stack_slots(self):
        extract_version = self.get_current_stack_version()
        if extract_version is not None:
            return extract_version["data"]
        else:
            return None

    def get_current_db_asset_version(self,  db_doc_obj=None):
        """

        Returns: database document of the current asset version that has one of the approved class statuses
        It will return None if there is no current version
        Uses the db_asset_id parent to get all children db_asset_versions and resolves to the current version

        """
        db_ops = CollectionOperators(db_collection=self.__context.project_publishes)

        doc_id = None

        if db_doc_obj is not None:
            if isinstance(db_doc_obj, DBAssetVersion) or isinstance(db_doc_obj, DBAsset) or isinstance(db_doc_obj, Asset):
                doc_id = db_doc_obj.id
            if isinstance(db_doc_obj, str):
                doc_id = db_doc_obj
            if isinstance(db_doc_obj, dict):
                doc_id = db_doc_obj["_id"]


            if doc_id is not None:
                version_parent = doc_id.rsplit(".", 1)[0]
                current_doc = db_ops.get_current_version(_id={"$regex": f"^{version_parent}"} )
                if len(current_doc) != 0:
                    return current_doc[0]
                else:
                    return None
            else:
                return None

        current_doc = db_ops.get_current_version(_id={"$regex": f"^{self.__context.db_asset_id}"})
        print(current_doc)
        if len(current_doc) != 0:
            return current_doc[0]
        else:
            return None
