import sys
import random
from pymongo import MongoClient
from PySide2.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem


class MongoDBAPI:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name, data):
        return self.db[collection_name].insert_one(data)

    def create_category_index(self, collection_name):
        self.db[collection_name].create_index([('category', 1)])

    def get_distinct_categories(self, collection_name):
        return self.db[collection_name].distinct("category")

    def get_assets_by_category(self, collection_name, category):
        return [doc['entry_name'] for doc in self.db[collection_name].find({"category": category}, {"entry_name": 1})]


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

    def get_categories(self):
        return self.api.get_distinct_categories(self.collection_name)

    def get_assets_by_category(self, category):
        return self.api.get_assets_by_category(self.collection_name, category)


class AssetLazyLoadView(QMainWindow):
    def __init__(self, view_model):
        super().__init__()

        self.view_model = view_model

        self.setWindowTitle("Lazy Loading Asset View")
        self.setGeometry(100, 100, 400, 300)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabel("Project Assets")
        self.setCentralWidget(self.tree_widget)

        self.tree_widget.itemExpanded.connect(self.load_assets_for_category)
        self.load_categories()

    def load_categories(self):
        self.categories = self.view_model.get_categories()
        for category in self.categories:
            QTreeWidgetItem(self.tree_widget, [category]).setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

    def load_assets_for_category(self, item):
        if item.childCount() == 0:
            category = item.text(0)
            assets = self.view_model.get_assets_by_category(category)
            for asset in assets:
                QTreeWidgetItem(item, [asset])


if __name__ == "__main__":
    app = QApplication([])

    mongo_api = MongoDBAPI("mongodb://localhost:27017", "Origin")
    mongo_api.create_category_index("build")


    asset_view_model = AssetViewModel(mongo_api, "shots")
    asset_lazy_load_view = AssetLazyLoadView(asset_view_model)

    # for _ in range(100000):
    #     category = random.choice(["characters", "props", "environment"])
    #     asset_name = f"Asset{random.randint(1, 100000)}"
    #     asset_view_model.insert_asset(asset_name, "Description", category)

    asset_lazy_load_view.show()

    sys.exit(app.exec_())
