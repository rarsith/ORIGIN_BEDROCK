from database import db_connection as mdbconn


class DbCollection(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

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