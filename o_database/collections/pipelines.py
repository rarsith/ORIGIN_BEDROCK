from typing import Any, Dict


class OriginDBPipelines:
    def __init__(self):
        self._skip: Any = None
        self._buffer: Any = None
        self._limit: Any = None
        self._sort: Any = None
        self._sort_attr: Any = None
        self._attribute_field: Any = None
        self._value_field: Any = None
        self._pipeline: Any = None

    @property
    def skip_op(self):
        return self._skip

    @skip_op.setter
    def skip_op(self, skip_val: int):
        self._skip = skip_val

    @property
    def buffer_op(self):
        return self._buffer

    @buffer_op.setter
    def buffer_op(self, buffer_val: list):
        self._buffer = buffer_val

    @property
    def limit_op(self):
        return self._limit

    @limit_op.setter
    def limit_op(self, limit_val: int):
        self._limit = limit_val

    @property
    def attribute_field(self):
        return self._attribute_field

    @attribute_field.setter
    def attribute_field(self, attrib_name: str):
        self._attribute_field = attrib_name

    @property
    def value_field(self):
        return self._value_field

    @value_field.setter
    def value_field(self, value: str):
        self._value_field = value

    @property
    def sort_docs(self):
        return self._sort

    @sort_docs.setter
    def sort_docs(self, value: int):
        self._sort = value

    @property
    def sort_attr(self):
        return self._sort_attr

    @sort_attr.setter
    def sort_attr(self, attr: str):
        self._sort_attr = attr

    def _create_match_stage(self, criteria):
        return {"$match": criteria}

    def generate_pipeline(self, criteria, ids_only=False):
        match_stage = self._create_match_stage(criteria)
        pipeline = [match_stage]

        if self._sort is not None:
            pipeline.append({"$sort": {self._sort_attr: self._sort}})
        if self._limit is not None:
            pipeline.append({"$limit": self._limit})
        if self._skip is not None:
            pipeline.append({"$skip": self._skip})

        if ids_only:
            pipeline.append({"$project": {"_id": 1}})

        return pipeline

    def criteria_value_startswith(self):
        """
        returns MongoDB filter for aggregation
        """
        if not isinstance(self._attribute_field, str):
            raise TypeError(f"{self._attribute_field} must be a of type string")

        criteria = {self._attribute_field: {"$regex": f"^{self._value_field}"}}

        return criteria

    def criteria_value_matches(self):
        """
        returns MongoDB filter for aggregation
        it returns the documents that have the field value matching exactly with the inputted :param sel_filter:

        Args:
            doc_field:
        """
        if not isinstance(self._attribute_field, str):
            raise TypeError(f"{self._attribute_field} must be a of type string")

        criteria = {self._attribute_field: self._value_field}

        return criteria

from pymongo import MongoClient

# Function to retrieve data by date
def get_data_by_date(db_name, collection_name):
    client = MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    pipeline = [
        {"$sort": {"date_field_name": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result

# Function to retrieve data by name
def get_data_by_name(db_name, collection_name):
    client = MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    pipeline = [
        {"$sort": {"name_field_name": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result

# Function to retrieve data by version
def get_data_by_version():
    db_O = MongoConnection().origin_production_database()
    collection_name = ProjectCollections().project_publishes_collection()
    collection = db_O[collection_name]

    pipeline = [
        {"$sort": {"version_cnt": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result

# Function to retrieve data by database path
def get_data_by_db_path():
    db_O = MongoConnection().origin_production_database()
    collection_name = ProjectCollections().project_publishes_collection()
    collection = db_O[collection_name]

    pipeline = [
        {"$sort": {"db_path_field_name": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result

def get_data_by_versionX():
    db_O = MongoConnection().origin_production_database()
    collection_name = ProjectCollections().project_publishes_collection()
    collection = db_O[collection_name]

    pipeline = [

        {"$match": {"parent_task": "concept"}},

        {"$group": {"_id": None, "max_version_cnt": {"$max": "$version_cnt"}}}

                ]

    result = list(collection.aggregate(pipeline))

    if result:
        max_version = result[0]["max_version_cnt"]

        documents = list(collection.find({"version_cnt": max_version}))
        return documents
    else:
        return []


if __name__ == "__main__":
    import pprint
    from o_database.collections.connections import ProjectCollections
    from o_database.mongo_connection import MongoConnection
    from envars.origin_envars import OriginEnvar

    OriginEnvar.show_name = "New_Era"
    db = MongoConnection().origin_production_database()

    collection_db = ProjectCollections().project_publishes_collection()

    orig_pipes = OriginDBPipelines()
    orig_pipes.attribute_field = "xxx"
    orig_pipes.value_field = "cucu.looku.mokku"


    crit = orig_pipes.criteria_value_startswith()
    crit02 = orig_pipes.criteria_value_matches()

    pipe1 = orig_pipes.generate_pipeline(crit)
    pipe2 = orig_pipes.generate_pipeline(crit02)
    print(pipe1)
    print(pipe2)
