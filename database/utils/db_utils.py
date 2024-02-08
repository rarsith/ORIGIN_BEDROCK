# class Combiner(object):
#     def __init__(self):
#         self.db = mdbconn.server[mdbconn.database_name]
#
#     def db_find_key(self, db_collection, item_to_search, **kwargs):
#         """
#         will find all the key values from a collection and returns them as a dictionary
#         """
#         items = []
#
#         cursor = self.db[db_collection]
#         results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
#         for result in results:
#             for k, v in result.items():
#                 items.append(v)
#         return items
#
#     def origin_update(self, entity_id, db_path, data=[]):
#         cursor = self.db[DbProjectBranch().get_type]
#         cursor.update_one({"_id": entity_id}, {"$set": {db_path: data}})
#
#     @classmethod
#     def combine(cls, *data, **kwargs):
#         if data:
#             id_elements = list()
#             for elem in data:
#                 id_elements.append(elem)
#             dotted_path = str(".".join(id_elements))
#             return dotted_path
#         return kwargs


