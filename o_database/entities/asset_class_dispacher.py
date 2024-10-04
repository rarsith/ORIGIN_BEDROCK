from o_database.entities.Xoperators import Asset, Group, Project, Task, CollectionOperators
from origin.envars.Xorigin_envars import ContextHandler

def __get_entity_class(item_type):
    if item_type == "group":
        return Group
    if item_type == "asset":
        return Asset
    if item_type == "project":
        return Project
    if item_type == "task":
        return Task

def extract_asset_class(context):
    context_handler = ContextHandler()
    context_handler.load_session(context)
    db_ops = CollectionOperators(db_collection=context_handler.show_name)
    entity_doc = db_ops.entity_document(doc_id=context_handler.entity_id)
    get_class = __get_entity_class(item_type=context_handler.entity_type)
    return get_class(**entity_doc)
