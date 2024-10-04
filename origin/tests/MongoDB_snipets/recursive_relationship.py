from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Origin']
collection = db['MooMoo']

# # Example documents
# documents = [
#     {"_id": 1, "parent": None, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
#     {"_id": 2, "parent": None, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
#     {"_id": 3, "parent": 1, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
#     {"_id": 4, "parent": 2, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
#     {"_id": 5, "parent": 3, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"}
# ]
#
# # Inserting documents into the collection
# collection.insert_many(documents)


documents = [
    {'_id': 'MooMoo', 'type': 'project', 'show_code': 'MooMoo-this is a code', 'entry_name': 'MooMoo', 'show_defaults': {}, 'active': True, 'date': '2024-02-13', 'time': '16:07', 'owner': 'arsithra', 'show_type': 'vfx', 'parent': None, 'visual_parent': None},
    {'_id': 'MooMoo.assets.characters.hulk', 'type': 'asset', 'entry_name': 'hulk', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': {}, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '16:17', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
    {'_id': 'MooMoo.assets.characters.red', 'type': 'asset', 'entry_name': 'red', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': None, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '18:28', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
    {'_id': 'MooMoo.assets.characters.blue', 'type': 'asset', 'entry_name': 'blue', 'origin_db_path': 'MooMoo.assets.characters', 'status': ' ', 'assignment': {}, 'assigned_to': [], 'tasks': {}, 'active': True, 'definition': 'TO FIX', 'date': '2024-02-13', 'time': '18:29', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets.characters'},
    {'_id': 'MooMoo.assets', 'type': 'group', 'entry_name': 'assets', 'origin_db_path': 'MooMoo', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:38', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo'},
    {'_id': 'MooMoo.assets.characters', 'type': 'group', 'entry_name': 'characters', 'origin_db_path': 'MooMoo.assets', 'definition': {}, 'data': {}, 'date': '2024-02-13', 'time': '18:47', 'owner': 'arsithra', 'parent': 'MooMoo', 'visual_parent': 'MooMoo.assets'}]



def get_all_in_collection():
    all_documents = collection.find({})
    return [document for document in all_documents]


documents = get_all_in_collection()
print(documents)
# for dic in documents:
#     print(dic)

def find_root(documents):
    for doc in documents:
        if doc["visual_parent"] is None:
            documents.remove(doc)
    return documents

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

    # for key, values in collapsed.items():
    #     new_dict = {key: values}
    #     regrouped_dict.append(new_dict)
    #
    # for pairs in regrouped_dict:
    #     if pairs.keys() in regrouped_dict:

    return collapsed


def pairs_to_dictionary(pairs_list):
    result = {}
    for key, value in pairs_list:

        result[key]=value

        # if key in result:
        #     result[key].append(value)
    return result


# Function to recursively find children
def find_children(document, parent_id):
    children = []
    for doc in document:
        if doc['visual_parent'] == parent_id:
            children.append(doc['entry_name'])
            children.extend(find_children(document, doc['_id']))
            # print("Found:", children)
    print(children)
    return children



def get_hierarchy(documents, parent_id=None):
    hierarchy = {}
    parents = []
    for doc in documents:
        if doc.get("visual_parent") is None and doc.get("visual_parent") not in hierarchy:
            hierarchy[doc.get("entry_name")] = {}
        else:
            # print(doc)
            parent_doc = get_dict_by_keyvalues(documents, "_id", doc["visual_parent"])
            if parent_doc["entry_name"] not in hierarchy:

                parents.append(parent_doc.get("entry_name"))

                # print("XXXX:", parent_doc["entry_name"])
    # print(hierarchy)


# print(documents)

# find_parents(documents)
#
# h = get_hierarchy(documents)


# Iterate over documents to find relationships
# relationships = {}
# for doc in documents:
#     if doc['visual_parent'] is not None:
#         relationships[doc['entry_name']] = find_children(documents, doc['_id'])

# Print relationships
# print(relationships)
