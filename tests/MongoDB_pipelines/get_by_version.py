from pymongo import MongoClient

# Function to retrieve data by version and get the greatest version
def get_data_by_version(db_name, collection_name):
    client = MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    pipeline = [
        {
            "$group": {
                "_id": None,
                "max_version": {"$max": "$version"}
            }
        }
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        max_version = result[0]["max_version"]
        # Now fetch the document(s) having this max version
        documents = list(collection.find({"version": max_version}))
        return documents
    else:
        return []
