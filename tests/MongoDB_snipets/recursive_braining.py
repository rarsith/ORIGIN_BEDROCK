


documents = [{'_id': 'MooMoo', 'type': 'project', 'show_code': 'MooMoo-this is a code', 'entry_name': 'MooMoo', 'show_defaults': {}, 'active': True, 'date': '2024-02-13', 'time': '16:07', 'owner': 'arsithra', 'show_type': 'vfx', 'parent': None, 'visual_parent': None},
{'_id': 'MooMoo.assets.characters.hulk', 'type': 'asset', 'entry_name': 'hulk', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': {}, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '16:17', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
{'_id': 'MooMoo.assets.characters.red', 'type': 'asset', 'entry_name': 'red', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': None, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '18:28', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
{'_id': 'MooMoo.assets.characters.blue', 'type': 'asset', 'entry_name': 'blue', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': {}, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '18:29', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
{'_id': 'MooMoo.assets', 'type': 'group', 'entry_name': 'assets', 'origin_db_path': 'MooMoo', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:38', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo'},
{'_id': 'MooMoo.assets.characters', 'type': 'group', 'entry_name': 'characters', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:47', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets'},
{'_id': 'MooMoo.assets.props', 'type': 'group', 'entry_name': 'props', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets'},
{'_id': 'MooMoo.assets.environments', 'type': 'group', 'entry_name': 'environments', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:51', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets'}]


def get_dict_by_keyvalues(dictionary_list, key, value):
    for dictionary in dictionary_list:
        if dictionary.get(key) == value:
            return dictionary
    return None

def find_parents(documents_list):
    parents = []
    collapsed = {}
    regrouped_dict = []

    def iterate_parents(parents_list):
        for document in parents_list:
            if document["visual_parent"] is not None:
                parent_doc = get_dict_by_keyvalues(documents, "_id", document["visual_parent"])
                parents.append(parent_doc)
                collapsed.setdefault(parent_doc["entry_name"], []).append(document["entry_name"])
    iterate_parents(documents_list)

    return collapsed



if __name__ == "__main__":
    import pprint

    get_h = find_parents(documents)
    print(get_h)

    # attempt to reorganize the resulting dictionary based on keys, if key is found in values

    def reorganize_dictionary(data: dict):
        reoganized = {}
        for keys, values in data.items():
            for other_keys, other_values in data.items():
                if keys in other_values:
                    reoganized[other_keys] = {keys:values}

        return reoganized

    reorganize_dict_h = reorganize_dictionary(get_h)
    print(reorganize_dict_h)
