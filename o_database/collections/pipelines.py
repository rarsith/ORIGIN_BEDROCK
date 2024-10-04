class OriginDBPipelines:

    def __init__(self):
        self._sort: list = []
        self._pipeline: list = []
        self._criteria: list = []

    @classmethod
    def _create_match_stage(cls, criteria: list):
        extended_criteria = [crit for crit in criteria]
        pipe = {"$match": {"$and": extended_criteria}}
        return pipe

    @classmethod
    def _create_sort_stage(cls, criteria: list):
        merged_terms = {key: value for crit in criteria for key, value in crit.items()}
        pipe = {"$sort": merged_terms}
        return pipe

    def create_pipeline(self):
        match_stage = self._create_match_stage(self._criteria)
        if len(self._sort) != 0:
            sort_stage = self._create_sort_stage(self._sort)
            self._pipeline.append(sort_stage)
        self._pipeline.insert(0, match_stage)
        return self._pipeline

    def add_attr_value_startswith(self, attribute_field: str, value_field: str):
        criteria = {attribute_field: {"$regex": f"^{value_field}"}}
        self._criteria.append(criteria)
        return criteria

    def add_match_attribute(self, attribute_field: str, value_field: str):
        criteria = {attribute_field: value_field}
        self._criteria.append(criteria)
        return criteria

    def add_sorting(self, sort_by_attr: str, sort_value: int):
        criteria = {"$sort": {sort_by_attr, sort_value}}
        self._pipeline.append(criteria)
        return criteria

    def add_sort(self, sort_by_attr: str, sort_value: int):
        criteria = {sort_by_attr:sort_value}
        self._sort.append(criteria)
        return criteria

    def add_limit(self, limit_value: int):
        criteria = {"$limit": limit_value}
        self._pipeline.append(criteria)
        return criteria

    def add_skip(self, skip_value: int):
        criteria = {"$skip": skip_value}
        self._pipeline.append(criteria)
        return criteria

    def ids_only(self, only_id: False):
        criteria = {"$project": {"_id": int(only_id)}}
        self._pipeline.append(criteria)
        return criteria

if __name__ == "__main__":
    from o_database.collections.Xconnections import ProjectCollections
    from o_database.mongo_connection import MongoConnection

    show_name = "New_State"
    db = MongoConnection().origin_production_database()

    collection_db = ProjectCollections(context=show_name).project_publishes_collection()
    print(collection_db)

    orig_pipes = OriginDBPipelines()
    orig_pipes.add_attr_value_startswith("_id", "New_State.assets.chr.red_hulk.red_hulk.modeling.main_pub")
    orig_pipes.add_match_attribute("type", "publish")
    orig_pipes.add_match_attribute("owner", "arsithra")

    # orig_pipes.add_limit(1)
    orig_pipes.add_sort("version_cnt", -1)
    # orig_pipes.ids_only(True)

    pipe = orig_pipes.create_pipeline()

    print(orig_pipes.create_pipeline())

    result_docs = db[collection_db].aggregate(pipe)
    print([doc["version_cnt"] for doc in result_docs])

"""
    [{'$match': {
        '$and': [{'_id': {'$regex': '^New_State.assets.chr.red_hulk.red_hulk.modeling.main_pub'}}, {'type': 'publish'},
                 {'owner': 'arsithra'}]}}, {'$match': {
        '$and': [{'_id': {'$regex': '^New_State.assets.chr.red_hulk.red_hulk.modeling.main_pub'}}, {'type': 'publish'},
                 {'owner': 'arsithra'}]}}, {'$limit': 1}, {'$sort': {'version_cnt': -1}},
     {'$sort': {'version_cnt': -1}}]

"""