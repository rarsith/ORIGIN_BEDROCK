from origin.common_utils import odb_path_resolver, json_utils

new_tasks_default_schemas = "new_tasks_default_schemas.json"
pub_slot_basic_schemas = "pub_slot_basic_schemas.json"
entities_definitions = "entities_definitions.json"


class EntityDefaultSchemas:

    @property
    def tasks(self):
        return _TaskSchemas()

    @property
    def output_slot(self):
        return _OutputSLotSchemas()

    @property
    def entry_definition(self):
        return _DefinitionSchemas()


class _TaskSchemas:

    @property
    def skeleton_schema(self):
        json_load = json_utils.open_json(odb_path_resolver.get_path(new_tasks_default_schemas))
        tasks_read = json_utils.read_dictionary(json_load, 'root')
        return tasks_read["task"]

    @property
    def character_schema(self):
        json_load = json_utils.open_json(odb_path_resolver.get_path(new_tasks_default_schemas))
        tasks_read = json_utils.read_dictionary(json_load, "character")
        return tasks_read["tasks"]

    @property
    def prop_schema(self):
        json_load = json_utils.open_json(odb_path_resolver.get_path(new_tasks_default_schemas))
        tasks_read = json_utils.read_dictionary(json_load, "prop")
        return tasks_read["tasks"]

    @property
    def environment_schema(self):
        json_load = json_utils.open_json(odb_path_resolver.get_path(new_tasks_default_schemas))
        tasks_read = json_utils.read_dictionary(json_load, "environment")
        return tasks_read["tasks"]

    @property
    def shot_schema(self):
        json_load = json_utils.open_json(odb_path_resolver.get_path(new_tasks_default_schemas))
        tasks_read = json_utils.read_dictionary(json_load, "shot")
        return tasks_read["tasks"]


class _OutputSLotSchemas:

    @property
    def skeleton_schema(self):
        json_load = json_utils.open_json(odb_path_resolver.get_path(pub_slot_basic_schemas))
        tasks_read = json_utils.read_dictionary(json_load, "pub_slot")
        return tasks_read


class _DefinitionSchemas:

    @property
    def skeleton_schema(self):
        json_load = json_utils.open_json(odb_path_resolver.get_path(entities_definitions))
        print(odb_path_resolver.get_path(entities_definitions))
        tasks_read = json_utils.read_dictionary(json_load, "base")
        return tasks_read



if __name__=="__main__":
    import pprint

    tt = EntityDefaultSchemas().entry_definition.skeleton_schema

    pprint.pprint (tt)