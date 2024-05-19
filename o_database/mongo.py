from database import db_connection as mdbconn
from o_database.mongo_connection import MongoConnection


class DBFind:
    def __init__(self, db_collection=None, entry_id=None, attribute=None):
        self.db = MongoConnection().origin_production_database()

        self.collection = db_collection
        self.entry_id = entry_id
        self.attribute = attribute

        self.result = self._db_results()

    def _db_results(self):
        results = self.db[self.collection].find({"_id": self.entry_id}, {"_id": 0, self.attribute: 1})
        return results

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
        for result in self.result:
            if delimiter in self.attribute:
                get_key = self.attribute.split(delimiter)[-1]
                get_value = self._find_key_value(result, get_key)
                return get_value
            return result[self.attribute]

    def attr_names(self):
        delimiter = "."
        for result in self.result:
            if delimiter in self.attribute:
                get_key = self.attribute.split(delimiter)[-1]
                get_value = self._find_key_value(result, get_key)
                return get_value
            return result[self.attribute]


class DBAdd:
    def __init__(self, db_collection, entry_id, attribute=None):
        self.db = MongoConnection().origin_production_database()

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
    def __init__(self, db_collection, entry_id, attribute=None):
        self.db = MongoConnection().origin_production_database()

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
    def __init__(self, db_collection, entry_id, attribute=None):
        self.db = MongoConnection().origin_production_database()

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
    def __init__(self, db_collection, entry_id, attribute=None):
        self.db = MongoConnection().origin_production_database()

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
