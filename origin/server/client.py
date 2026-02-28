# origin/api/client.py

import requests

from origin.database.entities.operators import get_entity_class

BRIDGE_URL = "http://127.0.0.1:8000"

def request_asset_creation(context, asset_name, asset_parent, options):
    """
    The Waiter: Takes the order from Maya and runs to the Kitchen.
    """
    payload = {
        "context": context.snapshot_session(),  # Our Dataclass converted to dict
        "asset_name": asset_name,
        "asset_parent": asset_parent,
        "options": options
    }

    try:
        response = requests.post(f"{BRIDGE_URL}/create/asset_with_tasks", json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def request_group_creation(context, group_name, group_parent):
    """
    The Waiter: Takes the order from Maya and runs to the Kitchen.
    """
    payload = {
        "context": context.snapshot_session(),  # Our Dataclass converted to dict
        "group_name": group_name,
        "group_parent": group_parent,
    }

    try:
        response = requests.post(f"{BRIDGE_URL}/create/group", json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def request_all_shows():
    result_objects = []

    try:
        response = requests.get(f"{BRIDGE_URL}/get/projects_names")
        for result in response.json().get("result"):
            result_objects.append(get_entity_class(result["type"])(**result))
        return result_objects

    except Exception as e:
        return {"status": "error", "message": str(e)}


def request_entity_children(context, entity_id):

    payload = {
        "context": context.snapshot_session(),
        "entity_id": entity_id,
    }

    result_objects = []

    try:
        response = requests.get(f"{BRIDGE_URL}/get/entity_children", json=payload)
        for result in response.json().get("result"):
            result_objects.append(get_entity_class(result["type"])(**result))
        return result_objects

    except Exception as e:
        return {"status": "error", "message": str(e)}