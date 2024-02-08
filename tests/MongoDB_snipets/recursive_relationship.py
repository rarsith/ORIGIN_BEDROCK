from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Origin']
collection = db['builds']

# Example documents
documents = [
    {"_id": 1, "parent": None, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
    {"_id": 2, "parent": None, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
    {"_id": 3, "parent": 1, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
    {"_id": 4, "parent": 2, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"},
    {"_id": 5, "parent": 3, "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5", "field6": "value6", "field7": "value7", "field8": "value8", "field9": "value9", "field10": "value10", "field11": "value11", "field12": "value12", "field13": "value13", "field14": "value14", "field15": "value15", "field16": "value16", "field17": "value17", "field18": "value18", "field19": "value19", "field20": "value20"}
]

# Inserting documents into the collection
collection.insert_many(documents)

# Function to recursively find children
def find_children(document, parent_id):
    children = []
    for doc in document:
        if doc['parent'] == parent_id:
            children.append(doc['_id'])
            children.extend(find_children(document, doc['_id']))
    return children

# Iterate over documents to find relationships
relationships = {}
for doc in documents:
    if doc['parent'] is None:
        relationships[doc['_id']] = find_children(documents, doc['_id'])

# Print relationships
print(relationships)
