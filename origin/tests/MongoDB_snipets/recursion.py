import pprint


dictionary_list = [
    {'_id': 'MooMoo', 'type': 'project', 'show_code': 'MooMoo-this is a code', 'entry_name': 'MooMoo', 'show_defaults': {}, 'active': True, 'date': '2024-02-13', 'time': '16:07', 'owner': 'arsithra', 'show_type': 'vfx', 'parent': None, 'visual_parent': None},
    {'_id': 'MooMoo.assets', 'type': 'group', 'entry_name': 'assets', 'origin_db_path': 'MooMoo', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:38', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo'},
    {'_id': 'MooMoo.sequences', 'type': 'group', 'entry_name': 'sequences', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo'},
    {'_id': 'MooMoo.sequences.templates', 'type': 'group', 'entry_name': 'templates', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo'},
    {'_id': 'MooMoo.project_control', 'type': 'group', 'entry_name': 'project_control', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo'},
    
    {'_id': 'MooMoo.assets.characters.hulk', 'type': 'asset', 'entry_name': 'hulk', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': {}, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '16:17', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
    {'_id': 'MooMoo.assets.characters.red', 'type': 'asset', 'entry_name': 'red', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': None, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '18:28', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
    {'_id': 'MooMoo.assets.characters.blue', 'type': 'asset', 'entry_name': 'blue', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': {}, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '18:29', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
    
    {'_id': 'MooMoo.assets.characters', 'type': 'group', 'entry_name': 'characters', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:47', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets'},
    {'_id': 'MooMoo.assets.props', 'type': 'group', 'entry_name': 'props', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets'},
    {'_id': 'MooMoo.assets.environments', 'type': 'group', 'entry_name': 'environments', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets'},
    {'_id': 'MooMoo.assets.characters.hulk.baby_hulk', 'type': 'group', 'entry_name': 'baby_hulk', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters.hulk'},
    {'_id': 'MooMoo.assets.environments.cave', 'type': 'asset', 'entry_name': 'cave', 'origin_db_path': 'MooMoo.assets.environments', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.environments'},
    {'_id': 'MooMoo.assets.props.knife', 'type': 'asset', 'entry_name': 'knife', 'origin_db_path': 'MooMoo.assets.props', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.props'},
    
    {'_id': 'MooMoo.sequences.RRC', 'type': 'group', 'entry_name': 'RRC', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.sequences'},
    {'_id': 'MooMoo.sequences.RRC.2020', 'type': 'group', 'entry_name': '2020', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.sequences.RRC'},
    {'_id': 'MooMoo.sequences.RRC.2030', 'type': 'group', 'entry_name': '2030', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.sequences.RRC'},
    
    
    {'_id': 'MooMoo.assets.characters.blue.baby_blue', 'type': 'group', 'entry_name': 'baby_blue', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters.blue'},
    {'_id': 'MooMoo.assets.characters.red.baby_red', 'type': 'group', 'entry_name': 'baby_red', 'origin_db_path': 'MooMoo.sequences', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters.red'}
]

def add_child(dictionary_list):
    new_dict_list = []
    for dictionary in dictionary_list:
        if "h_anchor" not in dictionary:
            dictionary["h_anchor"] = []
            new_dict_list.append(dictionary)
    
    return new_dict_list


def build_hierarchy(dictionary_list):
    
    new_dict = add_child(dictionary_list)

    dictionary_map = {d['_id']: d for d in new_dict}
    
    tree = {}
    
    for dictionary in dictionary_list:
        parent_id = dictionary.get("visual_parent")
        if parent_id is None:
            tree[dictionary["_id"]]=dictionary
        else:
            parent = dictionary_map.get(parent_id)
            if parent:
                parent["h_anchor"].append(dictionary)
    for keys, values in tree.items():
        return values


def extract_entry_names(data):
    tree = {}

    def deep_search(dictionary):
        if isinstance(dictionary, dict):
            entry_name = dictionary.get('entry_name')
            children = dictionary.get('h_anchor')
            catch = tree[entry_name] = [extract_entry_names(child) for child in children]

            return catch

    deep_search(data)

    return tree


def convert_to_dict(data):
    if isinstance(data, list):
        return {}
    result = {}
    for key, value in data.items():
        if isinstance(value, list):
            result[key] = {}
            for item in value:
                result[key].update(convert_to_dict(item))
        else:
            result[key] = convert_to_dict(value)
    return result


hierarchy = build_hierarchy(dictionary_list)
xxx = extract_entry_names(hierarchy)
ccc = convert_to_dict(xxx)
pprint.pprint(ccc)
