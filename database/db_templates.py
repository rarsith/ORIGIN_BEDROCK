from common_utils import json_utils
from common_utils import path_resolver


def show_structure():
    json_load = json_utils.open_json(path_resolver.get_path("show_default_schemas.json"))
    structure_read = json_utils.read_dictionary(json_load, 'structure')
    return structure_read


def task_defaults():
    json_load = json_utils.open_json(path_resolver.get_path("tasks_basic_schemas.json"))
    tasks_read = json_utils.read_dictionary(json_load, 'root')
    return tasks_read["task"]


def tasks_schema(category):
    json_load = json_utils.open_json(path_resolver.get_path("tasks_default_schemas.json"))
    tasks_read = json_utils.read_dictionary(json_load, category)
    return tasks_read["tasks"]


def tasks_pub_slot_schema():
    json_load = json_utils.open_json(path_resolver.get_path("pub_slot_basic_schemas.json"))
    tasks_read = json_utils.read_dictionary(json_load, "pub_slot")
    return tasks_read


def entry_definition(category):
    json_load = json_utils.open_json(path_resolver.get_path("entities_definitions.json"))
    tasks_read = json_utils.read_dictionary(json_load, category)
    return tasks_read["definition"]


if __name__=="__main__":
    import pprint

    tt = show_structure()
    tt = task_defaults()
    tt = tasks_schema(category="shot")
    pprint.pprint (tt)