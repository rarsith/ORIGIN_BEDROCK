from PySide2.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QAbstractItemView
)
from PySide2.QtCore import QEvent, Qt

class SingleDropTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Single Drop QTableWidget Example")
        self.setGeometry(100, 100, 400, 300)

        # Main widget container
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a QListWidget with some items
        self.list_widget = QListWidget()
        self.list_widget.addItems(["Item 1", "Item 2", "Item 3"])

        # Enable dragging from the QListWidget
        self.list_widget.setDragEnabled(True)

        # Create a QTableWidget with 2 columns and 2 rows
        self.table_widget = QTableWidget(2, 2)
        self.table_widget.setAcceptDrops(True)
        self.table_widget.setDragDropMode(QAbstractItemView.DropOnly)  # Table only accepts drops
        self.table_widget.viewport().installEventFilter(self)  # Install event filter on viewport

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.table_widget)
        main_widget.setLayout(layout)

        self.drop_allowed = True  # Flag to track if a drop has occurred

    def eventFilter(self, source, event):
        if event.type() == QEvent.Drop and self.drop_allowed:
            # Get drop position and target cell
            pos = event.pos()
            row = self.table_widget.rowAt(pos.y())
            column = self.table_widget.columnAt(pos.x())

            # Allow drop only in row 0, column 0
            if row == 0 and column == 0:
                item_text = self.list_widget.currentItem().text()
                self.table_widget.setItem(0, 0, QTableWidgetItem(item_text))
                self.drop_allowed = False  # Disable further drops
                return True  # Event handled

        # If the drop doesn't meet criteria or drop not allowed, ignore it
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication([])
    window = SingleDropTable()
    window.show()
    app.exec_()
