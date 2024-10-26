from origin.o_database.entities.Xoperators import CollectionOperators
from origin.o_database.entities.Xoperators import Project
from origin.o_database.entities.Xoperators import Asset
from origin.o_database.entities.Xoperators import Group
from origin.o_database.entities.Xoperators import Task
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


def extract_asset_class(context: ContextHandler):
    db_ops = CollectionOperators(db_collection=context.show_name)
    entity_doc = db_ops.entity_document(doc_id=context.entity_id)
    get_class = __get_entity_class(item_type=context.entity_type)
    return get_class(**entity_doc)
