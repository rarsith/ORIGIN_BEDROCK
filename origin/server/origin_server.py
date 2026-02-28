from fastapi import FastAPI, Body
from origin.database.entities.actions import Create
from origin.database.entities.operators import Projects, Project
from origin.database.mongo import CollectionOperators
from origin.database.schemas.templates.tasks_templates import TasksTemplates
from origin.envars.origin_envars import ContextHandler, OriginDatabaseHandler

app = FastAPI()


def get_db(payload: dict):
    """
    A single helper to 'unlock' the database from a network request.
    """
    ctx_data = payload.get("context")
    ctx = ContextHandler().load_session(ctx_data)
    return OriginDatabaseHandler(context=ctx)


@app.get("/get/db_document_by_id")
def get_db_document_by_id(payload: dict = Body(...)):
    db_collection, doc_id = [0,0]
    db_ops = CollectionOperators(db_collection=db_collection)
    document = db_ops.entity_document(doc_id=doc_id)
    # document_object = get_entity_class(item_type=document['type'])(**document)
    # print(document_object.type)
    return document


@app.post("/create/asset_with_tasks")
def api_create_asset(payload: dict = Body(...)):
    """
    The Chef: This receives the 'Order Slip' and does the heavy work.
    """
    # 1. Unpack the Order Slip
    ctx_dict = payload.get("context")
    asset_name = payload.get("asset_name")
    asset_parent = payload.get("asset_parent")
    options = payload.get("options", [])  # e.g. ["has_groom"]

    # 2. Reconstruct the Context
    context_handler = ContextHandler()
    context_handler.load_session(session_data=ctx_dict)


    # 3. DO THE WORK (Exactly like your original code, but here in 3.10)
    created_asset_id = Create(context=context_handler).asset(name=asset_name, parent=asset_parent)

    # Update context with the new ID for the tasks
    context_handler.entity_id = created_asset_id

    tasks_template = TasksTemplates(context=context_handler)
    tasks_template.build_base_task_schema()

    # Apply options
    options_config = {
        "has_groom": tasks_template.build_has_groom,
        "has_groom_cfx": tasks_template.build_has_groom_cfx,
        "has_cloth_cfx": tasks_template.build_has_cloth_cfx,
        "is_assembly": tasks_template.build_is_assembly,
    }

    for opt in options:
        if opt in options_config:
            options_config[opt]()

    tasks_template.create_build_tasks()

    return {"status": "success", "created_id": created_asset_id}


@app.post("/create/group")
def api_create_group(payload: dict = Body(...)):
    """
    The Chef: This receives the 'Order Slip' and does the heavy work.
    """

    ctx_dict = payload.get("context")
    group_name = payload.get("group_name")
    group_parent = payload.get("group_parent")

    context_handler = ContextHandler()
    context_handler.load_session(session_data=ctx_dict)

    created_group_id = Create(context=context_handler).group(name=group_name, parent=group_parent)

    return {"status": "success", "created_id": created_group_id}


@app.get("/get/projects_names")
def api_get_projects_names():
    get_all_shows = Projects().names()
    if get_all_shows is None:
        return None

    all_shows = [show for show in get_all_shows]
    return {"result" : all_shows} #all_shows


@app.get("/get/entity_children")
def api_get_entity_children(payload: dict = Body(...)):

    entity_id = payload.get("entity_id")
    ctx = payload.get("context")

    context_handler = ContextHandler()
    context_handler.load_session(session_data=ctx)

    children = []
    doc_data = CollectionOperators(db_collection=context_handler.show_name)
    children_docs = doc_data.children_with_parent_id(parent_id=entity_id)
    for child in children_docs:
        children.append(child)
    return {"result" : children}


