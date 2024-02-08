import sys
from pymongo import MongoClient
from PySide2.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem


class MongoDBAPI:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def get_assets_by_category(self):
        assets_by_category = {}
        assets = self.db['assets'].find({}, {'category': 1, 'name': 1})

        for asset in assets:
            category = asset['category']
            asset_name = asset['name']

            if category not in assets_by_category:
                assets_by_category[category] = []

            assets_by_category[category].append(asset_name)

        return assets_by_category


class AssetTreeView(QMainWindow):
    def __init__(self, categories):
        super().__init__()

        self.setWindowTitle("Asset Tree View")
        self.setGeometry(100, 100, 400, 300)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabel("Project Assets")
        self.setCentralWidget(self.tree_widget)

        self.populate_tree(categories)

    def populate_tree(self, categories):
        for category, assets in categories.items():
            category_item = QTreeWidgetItem(self.tree_widget, [category])

            for asset in assets:
                asset_item = QTreeWidgetItem(category_item, [asset])


if __name__ == "__main__":
    app = QApplication([])

    mongo_api = MongoDBAPI("mongodb://localhost:27017", "your_database_name")
    categories = mongo_api.get_assets_by_category()

    asset_tree_view = AssetTreeView(categories)
    asset_tree_view.show()

    sys.exit(app.exec_())