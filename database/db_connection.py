from o_database.mongo_connection import MongoConnection

# connection_test = server[database_name]
# print(connection_test["RED"].insert_one({"CRAAAP":"SHIIIIT"}))


if __name__ == "__main__":
    prod_database_conn = MongoConnection().origin_production_database()
    users_database_conn = MongoConnection().origin_users_database()
    setup_database_conn = MongoConnection().origin_setup_database()

