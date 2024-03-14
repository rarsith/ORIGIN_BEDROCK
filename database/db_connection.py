from pymongo import MongoClient



server = MongoClient('mongodb://localhost:27017')
database_name = "Origin"
# connection_test = server[database_name]
# print(connection_test["RED"].insert_one({"CRAAAP":"SHIIIIT"}))


class MongoConnection:

    def __init__(self):
        self.host = 'localhost'
        self.port = 27017
        self.production_database = 'Origin_Celestis'
        self.setup_database = 'Origin_Setup'
        self.users_database = 'Origin_Users'
        self.client = None
        self.db = None


    def _connect(self):
        self.client = MongoClient(self.host, self.port)[self.production_database]
        return self

    def _select_database(self, db_name):
        if self.client:
            self.db = self.client[db_name]
            return self.db

    def origin_production_database(self):
        self.client = MongoClient(self.host, self.port)[self.production_database]
        return self.client

    def origin_users_database(self):
        self.client = MongoClient(self.host, self.port)[self.users_database]
        return self.client

    def origin_setup_database(self):
        self.client = MongoClient(self.host, self.port)[self.setup_database]
        return self.client


if __name__ == "__main__":
    prod_database_conn = MongoConnection().origin_production_database()
    users_database_conn = MongoConnection().origin_users_database()
    setup_database_conn = MongoConnection().origin_setup_database()

