from typing import List, Dict, Union, Any

from origin.database.collections.pipelines import OriginDBPipelines
from origin.database.mongo_connection import MongoConnection


class DBFind:
    def __init__(self, database=None, db_collection=None, entry_id=None, attribute=None):
        self.db = MongoConnection().origin_production_database()

        if database is not None:
            self.db = database

        self.collection = db_collection
        self.entry_id = entry_id
        self.attribute = attribute

        self.result = self._db_results()

    def _db_results(self):
        results = self.db[self.collection].find({"_id": self.entry_id}, {"_id": 0, self.attribute: 1})
        if results:
            return results
        else:
            return None

    def _find_key_value(self, dictionary, target_key):
        for key, value in dictionary.items():
            if key == target_key:
                return value
            elif isinstance(value, dict):
                result = self._find_key_value(value, target_key)
                if result is not None:
                    return result
        return None

    def attr_values(self):
        delimiter = "."
        if self.result is not None:
            for result in self.result:
                if delimiter in self.attribute:
                    get_key = self.attribute.split(delimiter)[-1]
                    get_value = self._find_key_value(result, get_key)
                    return get_value
                else:
                    return result[self.attribute]
        else:
            return None

    def attr_names(self):
        delimiter = "."
        for result in self.result:
            if delimiter in self.attribute:
                get_key = self.attribute.split(delimiter)[-1]
                get_value = self._find_key_value(result, get_key)
                return get_value
            return result[self.attribute]


class DBAdd:
    def __init__(self, database=None, db_collection=None, entry_id=None, attribute=None):
        self.db = MongoConnection().origin_production_database()

        if database is not None:
            self.db = database

        self.collection = db_collection
        self.entry_id = entry_id
        self.attribute = attribute

    def value_to_field(self, data) -> None:
        """
        Add a value to an already existing list of Values. Checks if the value is already in.
        if True, the new value/values will not be added.
        Args:
            data:

        Returns:

        """
        check_if_exists = DBFind(self.collection, self.entry_id, self.attribute).attr_values()

        if check_if_exists is None:
            DBSet(self.collection, self.entry_id, self.attribute).attribute_value(data=[data])
            check_if_exists = DBFind(self.collection, self.entry_id, self.attribute).attr_values()

        if not isinstance(data, list):
            if data not in check_if_exists:
                self.db[self.collection].update_one({"_id": self.entry_id}, {"$push": {self.attribute: data}})
            else:
                print(f"{data} already exists, NOTHING DONE!")

        else:
            for each in data:
                if each not in check_if_exists:
                    self.db[self.collection].update_one({"_id": self.entry_id}, {"$push": {self.attribute: each}})
                else:
                    print(f"{each} already exists, NOTHING DONE!")

    def attribute_to_document(self, attr_name, attr_value={}):
        if attr_value is None:
            value_to_enter = {}
        else:
            value_to_enter = attr_value

        insert_path = ".".join([self.attribute, attr_name])
        self.db[self.collection].update_one({"_id": self.entry_id}, {"$set": {insert_path: value_to_enter}})
        return insert_path


class DBSet:
    def __init__(self, database=None, db_collection=None, entry_id=None, attribute=None):
        self.db = MongoConnection().origin_production_database()

        if database is not None:
            self.db = database

        self.collection = db_collection
        self.entry_id = entry_id
        self.attribute = attribute

    def attribute_value(self, data) -> None:
        """
        Changes an existing value to the new one. Does not ADD a new value
        Args:
            data:

        Returns:

        """
        self.db[self.collection].update_one({"_id": self.entry_id}, {"$set": {self.attribute: data}})


class DBClear:
    def __init__(self, database=None, db_collection=None, entry_id=None, attribute=None):
        self.db = MongoConnection().origin_production_database()

        if database is not None:
            self.db = database

        self.collection = db_collection
        self.entry_id = entry_id
        self.attribute = attribute

    def _attribute_type(self):
        target_attr = f"${self.attribute}"
        find_attr = [{"$match": {"_id": self.entry_id}}, {"$project": {"fieldType": {"$type": target_attr}}}]
        type_is = self.db[self.collection].aggregate(find_attr)

        for attr in type_is:
            return attr["fieldType"]

    def _attribute_type_switch(self, attr_type):
        if attr_type == "array":
            return []
        elif attr_type == "object":
            return {}
        elif attr_type == "string":
            return ""

    def attribute_values(self, override_type=[], override=False):
        """Removes the full content of an attribute by first removing the full atrribute and then recreating it empty"""
        attr_type = self._attribute_type()
        update_attr = self._attribute_type_switch(attr_type)

        self.db[self.collection].update_one({"_id": self.entry_id}, {"$unset": {self.attribute: 1}})

        if override:
            self.db[self.collection].update_one({"_id": self.entry_id}, {"$set": {self.attribute: override_type}})
        else:
            self.db[self.collection].update_one({"_id": self.entry_id}, {"$set": {self.attribute: update_attr}})


class DBRemove:
    def __init__(self, database=None, db_collection=None, entry_id=None, attribute=None):
        self.db = MongoConnection().origin_production_database()

        if database is not None:
            self.db = database

        self.collection = db_collection
        self.entry_id = entry_id
        self.attribute = attribute

    def _attribute_type(self):
        target_attr = f"${self.attribute}"
        find_attr = [{"$match": {"_id": self.entry_id}}, {"$project": {"fieldType": {"$type": target_attr}}}]
        type_is = self.db[self.collection].aggregate(find_attr)

        for attr in type_is:
            return attr["fieldType"]

    def _attribute_type_switch(self, attr_type):
        if attr_type == "array":
            return []
        elif attr_type == "object":
            return {}
        elif attr_type == "string":
            return ""

    def attribute_from_document(self):
        self.db[self.collection].update_one({"_id": self.entry_id}, {"$unset": {self.attribute: 1}})

    def attribute_value(self, data):
        self.db[self.collection].update_one({"_id": self.entry_id}, {"$set": {self.attribute: data}})

    def value_from_array(self, value):
        self.db[self.collection].update_one({"_id": self.entry_id}, {"$pull": {self.attribute: value}})


class DBDelete:
    def __init__(self, database=None, db_collection=None, entry_id=None):
        self.db = MongoConnection().origin_production_database()

        if database is not None:
            self.db = database

        self.collection = db_collection
        self.entry_id = entry_id

    def document(self):
        self.db[self.collection].delete_one({"_id": self.entry_id})


class CollectionOperators:

    def __init__(self, db_collection=None, database=None):
        self.db = MongoConnection().origin_production_database()

        if database is not None:
            self.db = database

        if db_collection is None or len(db_collection) == 0:
            self.collection_name = "empty"
        else:
            self.collection_name = db_collection

        self.db_collection = self.db[self.collection_name]

    def get_multiple_documents(self, doc_attr=None, **kwargs):
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

    def children_with_parent_id(self, parent_id):
        db_documents = self.db_collection.find({"parent": parent_id})
        return [doc for doc in db_documents]

    def entities_attr_value_starts_with(self, attr_field: str, val_starts_with: str, extra_filters: List[dict] = None,
                                        ids_only=False):

        pipe = OriginDBPipelines()
        pipe.add_attr_value_startswith(attribute_field=attr_field, value_field=val_starts_with)

        pipe.add_sort(sort_by_attr="time", sort_value=-1)
        pipe.add_sort(sort_by_attr="date", sort_value=-1)

        if extra_filters:
            for ex_filter in extra_filters:
                pipe.add_match_attribute_dict(ex_filter)

        if ids_only:
            pipe.ids_only(only_id=ids_only)

        pipeline = pipe.create_pipeline()

        try:
            if self.db_collection is not None:
                results = list(self.db_collection.aggregate(pipeline))
                return results

        except Exception as e:
            print(__file__, e)

    def get_all_versions(self, db_asset, published_by: str = None):
        pipe = OriginDBPipelines()
        pipe.add_attr_value_startswith(db_asset.ID, db_asset.id)
        pipe.add_match_attribute(db_asset.TYPE, "publish")

        if published_by is not None:
            pipe.add_match_attribute(db_asset.OWNER, published_by)

        pipe.add_sort("version_cnt", -1)
        pipeline = pipe.create_pipeline()

        try:
            if self.db_collection is not None:
                results = list(self.db_collection.aggregate(pipeline))
                return results

        except Exception as e:
            print(__file__, e)

    def get_all_file_components(self, db_asset_version, published_by: str = None):
        pipe = OriginDBPipelines()
        pipe.add_attr_value_startswith(db_asset_version.ID, db_asset_version.id)
        pipe.add_match_attribute(db_asset_version.TYPE, "publish")

        if published_by is not None:
            pipe.add_match_attribute(db_asset_version.OWNER, published_by)

        pipe.add_sort("version_cnt", -1)
        pipeline = pipe.create_pipeline()

        try:
            if self.db_collection is not None:
                results = list(self.db_collection.aggregate(pipeline))
                return results

        except Exception as e:
            print(__file__, e)

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
