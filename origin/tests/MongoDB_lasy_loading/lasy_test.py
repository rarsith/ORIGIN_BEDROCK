from pymongo import MongoClient
import random
import string

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['test_database']
collection = db['test_collection']


# Function to generate random string
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Create 10 documents with random children
for i in range(10):
    parent_doc = {"name": f"Document_{i}", "children": []}
    parent_id = collection.insert_one(parent_doc).inserted_id

    # Generate random number of children references
    num_children = random.randint(1, 5)
    existing_ids = set([parent_id])  # Avoid referencing itself
    for _ in range(num_children):
        child_id = parent_id
        while child_id == parent_id or child_id in parent_doc['children']:
            child_id = random.choice(list(existing_ids))
        parent_doc['children'].append(child_id)
        collection.update_one({"_id": parent_id}, {"$set": {"children": parent_doc['children']}})
        existing_ids.add(child_id)

print("Documents inserted successfully.")
