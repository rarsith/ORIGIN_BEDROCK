from PySide2.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QWidget
import pymongo

# Assuming you've established a connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Corpse"]
collection = db["fufu"]

# Example function to fetch documents for a specific page
def fetch_documents(page_number, items_per_page):
    skip = (page_number - 1) * items_per_page
    documents = collection.find().skip(skip).limit(items_per_page)
    return documents

# Example function to populate the QTreeWidget with documents
def populate_tree(tree, documents):
    tree.clear()
    for document in documents:
        item = QTreeWidgetItem(tree)
        item.setText(0, document["field1"])
        item.setText(1, document["field2"])

app = QApplication([])

tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["Field 1", "Field 2"])

# Function to handle next button click event
def next_page(current_page):
    current_page[0] += 1
    populate_tree(tree, fetch_documents(current_page[0], items_per_page))

# Function to handle previous button click event
def prev_page(current_page):
    current_page[0] -= 1
    populate_tree(tree, fetch_documents(current_page[0], items_per_page))

# Assuming items_per_page and total_count are predefined
items_per_page = 10
total_count = collection.count_documents({})  # Get total count of documents in the collection
num_pages = (total_count + items_per_page - 1) // items_per_page
current_page = [1]  # Using a list to store current page

next_button = QPushButton("Next")
next_button.clicked.connect(lambda: next_page(current_page))

prev_button = QPushButton("Previous")
prev_button.clicked.connect(lambda: prev_page(current_page))

# Initially populate the tree with documents from the first page
populate_tree(tree, fetch_documents(current_page[0], items_per_page))

layout = QVBoxLayout()
layout.addWidget(tree)
layout.addWidget(prev_button)
layout.addWidget(next_button)

window = QWidget()
window.setLayout(layout)
window.show()

app.exec_()
