import sys
from pymongo import MongoClient
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class MongoDBAPI:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name, data):
        return self.db[collection_name].insert_one(data)


class AssetSchema:
    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category
        }


class AssetViewModel:
    def __init__(self, api, collection_name):
        self.api = api
        self.collection_name = collection_name

    def insert_asset(self, name, description, category):
        new_asset_schema = AssetSchema(name=name, description=description, category=category)
        return self.api.insert_document(self.collection_name, new_asset_schema.to_dict())


class AssetView(QWidget):
    def __init__(self, view_model):
        super().__init__()

        self.view_model = view_model

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.category_input = QLineEdit(self)

        self.submit_button = QPushButton("Insert Asset", self)
        self.submit_button.clicked.connect(self.insert_asset)

        self.layout.addWidget(QLabel("Name:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Description:"))
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(QLabel("Category:"))
        self.layout.addWidget(self.category_input)
        self.layout.addWidget(self.submit_button)

    def insert_asset(self):
        name = self.name_input.text()
        description = self.description_input.text()
        category = self.category_input.text()

        inserted_id = self.view_model.insert_asset(name, description, category)
        print("Insert result:", inserted_id)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mongo_api = MongoDBAPI("mongodb://localhost:27017", "your_database_name")
    asset_view_model = AssetViewModel(mongo_api, "assets")
    asset_view = AssetView(asset_view_model)

    asset_view.show()
    sys.exit(app.exec_())
