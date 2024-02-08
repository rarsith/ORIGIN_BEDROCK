from pymongo import MongoClient

# Constants
DB_URI = "mongodb://localhost:27017/"
DB_NAME = "your_db_name"

# Database Connection Wrapper
class Database:
    def __init__(self, db_uri, db_name):
        # Establish a connection to the MongoDB server and select the database
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

# DbRef Class
class DbRef:
    def __init__(self, collection="", entity_id=""):
        # Store collection and entity_id for reference creation
        self.collection = collection
        self.entity_id = entity_id

    # ... (rest of the DbRef implementation)

# Collection Locator
class CollectionLocator:
    def __init__(self, db):
        # Store the database instance for collection retrieval
        self.db = db

    def get_collection(self, collection_name):
        return self.db[collection_name]

# Query Entity
class QueryEntity:
    def __init__(self, db, collection_locator):
        # Store the database and collection_locator instances for querying
        self.db = db
        self.collection_locator = collection_locator

    def create_for_collection(self, collection_name):
        # Create a QueryEntity instance for a specific collection
        collection = self.collection_locator.get_collection(collection_name)
        return QueryEntity(self.db, self.collection_locator)

    # ... (rest of the QueryEntity implementation)

# Entry Point
if __name__ == '__main__':
    from envars.envars import Envars

    # Initialize database
    db = Database(DB_URI, DB_NAME)

    # Initialize components
    collection_locator = CollectionLocator(db)
    query_entity = QueryEntity(db, collection_locator)

    # Set Envars values
    Envars.show_name = "Green"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "frog"
    Envars.task_name = "groom"

    # Usage examples using refactored components
    build_qentity = query_entity.create_for_collection("builds")

    # Retrieve tasks list for a specific condition
    tasks_list = build_qentity.get_all_ids_collection(condition={"show_name": Envars().show_name})

    # Print the resulting tasks list
    print("Task IDs for show '{}':".format(Envars().show_name))
    for task in tasks_list:
        print(task)
