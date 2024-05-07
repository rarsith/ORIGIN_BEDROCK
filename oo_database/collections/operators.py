import o_database.mongo_connection
from database import db_connection as mdbconn
from o_database.mongo_connection import MongoConnection
from o_database.collections.pipelines import OriginDBPipelines


class FindInCollection:
    def __init__(self):
        self.db = MongoConnection().origin_production_database()

    def all_collections(self):
        all_collections_in_database = self.db.list_collection_names()
        return all_collections_in_database

    def get_documents(self, db_collection: str, pipeline: OriginDBPipelines) -> list:
        """
        based on the sel_names param, returns a list MongoDB documents (full)
        Example for sel_names param: ""
        :return:

        Args:
            db_collection:
            pipeline:
            doc_field:

        """
        result = list(self.db[db_collection].aggregate(pipeline))

        return result


class DbRef:
    def __init__(self, collection="", entity_id=""):
        self.collection = collection
        self.entity_id = entity_id
        self.db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]

    @property
    def db_ref(self):
        gen_id = ",".join([self.collection, self.entity_id])
        return str(gen_id)

    def db_deref(self, ref_string, get_field=None):
        extr_collection, extr_entity_id = ref_string.split(",")
        if not get_field:
            return extr_collection, extr_entity_id
        elif get_field:
            cursor = self.db[extr_collection]
            db_field = cursor.find_one({"_id":extr_entity_id})
            return db_field[get_field]


class DbReferences:
    def __init__(self):
        self.db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]

    @classmethod
    def add_db_id_reference(cls, collection, parent_doc_id, destination_slot, id_to_add, from_collection, replace=False):
        db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]
        if not replace:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$push": {destination_slot: DbRef(from_collection, id_to_add).db_ref}})
        else:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$set": {destination_slot: DbRef(from_collection, id_to_add).db_ref}})

    def get_db_referenced_attr(self, src_collection, src_id, src_attr, attr_to_find):
        list_attr = list()
        if not src_id or src_id == None:
            return
        else:
            id_list = self.db[src_collection].find_one({"_id": src_id})
            for each_id in id_list[src_attr]:
                attr_data = DbRef().db_deref(each_id, attr_to_find)
                list_attr.append(attr_data)
            return list_attr


class DbCollection(object):
    def __init__(self):
        self.db = o_database.mongo_connection.server[o_database.mongo_connection.database_name]

    def db_add(self, db_collection, **kwargs) -> None:
        """
        will add a new entry to a collection
        """
        cursor = self.db[db_collection]
        cursor.insert_one(kwargs)

    def db_find(self, db_collection, item_to_search, **kwargs) -> list:
        """
        will find all the key values from a collection and returns them as a dictionary
        """
        items = []
        cursor = self.db[db_collection]
        results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
        for result in results:
            for k, v in result.items():
                items.append(v)

        return items

    def db_find_kk(self, db_collection, item_to_search, **kwargs) -> list:
        """
        will find all the key values from a collection and returns them as a dictionary
        """
        cursor = self.db[db_collection]
        results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
        for result in results:
            return result
