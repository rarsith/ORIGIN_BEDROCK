from origin.database.mongo import CollectionOperators
from origin.database.entities.operators import Project
from origin.database.entities.operators import Asset
from origin.database.entities.operators import Group
from origin.database.entities.operators import Task
from origin.envars.origin_envars import ContextHandler

def __get_entity_class(item_type):
    if item_type == "group":
        return Group
    if item_type == "asset":
        return Asset
    if item_type == "project":
        return Project
    if item_type == "task":
        return Task


def extract_asset_class(context: ContextHandler):
    db_ops = CollectionOperators(db_collection=context.show_name)
    entity_doc = db_ops.entity_document(doc_id=context.entity_id)
    get_class = __get_entity_class(item_type=context.entity_type)
    return get_class(**entity_doc)
