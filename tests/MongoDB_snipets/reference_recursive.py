from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Origin']
collection = db['MooMoo']


def build_hierarchy(dictionary_list):
    # Step 1: Build a mapping of dictionary identifiers to dictionaries
    dictionary_map = {d['_id']: d for d in dictionary_list}

    # Step 2: Construct the tree structure
    tree = {}
    for dictionary in dictionary_list:
        parent_id = dictionary.get('visual_parent')
        if parent_id is None:
            tree[dictionary['_id']] = dictionary
        else:
            parent = dictionary_map.get(parent_id)
            if parent:
                if 'children' not in parent:
                    parent['children'] = []
                parent['children'].append(dictionary)
            else:
                print(f"Parent with id '{parent_id}' not found for dictionary with id '{dictionary['id']}'")

    return tree


def print_hierarchy(node, depth=0):
    if isinstance(node, dict):
        print("  " * depth + f"- {node['entry_name']} ({node['_id']})")
        if 'children' in node:
            for child in node['children']:
                print_hierarchy(child, depth + 1)


def get_all_in_collection():
    all_documents = collection.find({})
    docs = [document for document in all_documents]
    for d in docs:
        print(d)
    return [document for document in all_documents]

import pprint
dictionary_list = get_all_in_collection()
pprint.pprint(dictionary_list)

# Example list of dictionaries
# dictionary_list = [
#     {'id': '1', 'name': 'Parent A', 'parent_id': None},
#     {'id': '2', 'name': 'Child A1', 'parent_id': '1'},
#     {'id': '3', 'name': 'Child A2', 'parent_id': '1'},
#     {'id': '4', 'name': 'Grandchild A2.1', 'parent_id': '3'},
#     {'id': '5', 'name': 'Parent B', 'parent_id': None},
#     {'id': '6', 'name': 'Child B1', 'parent_id': '5'},
#     {'id': '7', 'name': 'Child B2', 'parent_id': '5'},
# ]

# # Step 3: Build the hierarchy and print it
# hierarchy = build_hierarchy(dictionary_list)
# pprint.pprint(hierarchy)
# for root_node in hierarchy.values():
#     print_hierarchy(root_node)