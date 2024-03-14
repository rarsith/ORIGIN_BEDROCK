import pymongo


class MongoDBConnection:
    def __init__(self, host='localhost', port=27017, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.db = None

        self.connect()

    def connect(self):
        try:
            if self.username and self.password:
                self.client = pymongo.MongoClient(self.host, self.port, username=self.username, password=self.password)
            else:
                self.client = pymongo.MongoClient(self.host, self.port)
            return self
        except pymongo.errors.ConnectionFailure as e:
            print("Could not connect to MongoDB: %s" % e)
            return None

    def select_database(self, db_name):
        if self.client:
            self.db = self.client[db_name]
            return self
        else:
            print("Connection not established.")
            return None

    def connect_to_main_database(self):
        return self.select_database('Origin')

    def connect_to_secondary_database(self):
        return self.select_database('Origin')

# Example usage:
# Initialize connection parameters
host = 'localhost'
port = 27017
username = 'your_username'
password = 'your_password'

# Connect to the main database
# mongo_connection = MongoDBConnection(host, port, username, password).connect_to_main_database()

# Check if connection is successful
# if mongo_connection:
#     print("Connected to main database successfully!")

    # Now you can use the 'mongo_connection' object to interact with the selected database

# Connect to the secondary database
mongo_connection = MongoDBConnection(host, port).connect_to_secondary_database()

# Check if connection is successful
if mongo_connection:
    print("Connected to secondary database successfully!")

    # Now you can use the 'mongo_connection' object to interact with the selected database
