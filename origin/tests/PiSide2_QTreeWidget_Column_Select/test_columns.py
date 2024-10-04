import sys
import random
from PySide2.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QDialog, QMenu, QAction, QCheckBox

class ColumnSelectDialog(QDialog):
    def __init__(self, tree_widget, parent=None):
        super(ColumnSelectDialog, self).__init__(parent)
        self.tree_widget = tree_widget
        self.setWindowTitle("Select Columns")
        self.layout = QVBoxLayout(self)
        self.checkboxes = []
        self.create_checkboxes()

    def create_checkboxes(self):
        columns = self.tree_widget.columnCount()
        for i in range(columns):
            column_name = self.tree_widget.headerItem().text(i)
            checkbox = QCheckBox(column_name, self)
            checkbox.setChecked(not self.tree_widget.isColumnHidden(i))
            checkbox.stateChanged.connect(lambda state, col=i: self.toggle_column(col, state))
            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

    def toggle_column(self, column, state):
        self.tree_widget.setColumnHidden(column, not state)

app = QApplication([])

# Create a QTreeWidget
tree_widget = QTreeWidget()
tree_widget.setColumnCount(7)

# Generate random column names
column_names = [f"Column {i+1}" for i in range(7)]
tree_widget.setHeaderLabels(column_names)

# Populate tree widget with random data
for _ in range(10):
    item = QTreeWidgetItem(tree_widget)
    for i in range(7):
        item.setText(i, f"Item {random.randint(1, 100)}")

# Create a menu
menu = ColumnSelectDialog(tree_widget)

# Create a QPushButton to show the menu
button = QPushButton("Show Menu")
button.clicked.connect(menu.exec_)

# Show the button and tree widget
button.show()
tree_widget.show()

# Run the application
sys.exit(app.exec_())