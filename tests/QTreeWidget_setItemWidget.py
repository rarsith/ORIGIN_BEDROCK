import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(3)

        header = ["Column 1", "Column 2", "Column 3"]
        self.treeWidget.setHeaderLabels(header)

        # Add some items to the tree
        for i in range(5):
            item = QTreeWidgetItem(["", "", ""])
            self.treeWidget.addTopLevelItem(item)

            # Create widgets for each column
            for col in range(3):
                widget = QWidget()
                layout = QVBoxLayout()
                widget.setLayout(layout)

                label = QLabel(f"Label {col}")
                lineEdit = QLineEdit(f"Edit {col}")

                layout.addWidget(label)
                layout.addWidget(lineEdit)

                self.treeWidget.setItemWidget(item, col, widget)

        self.setCentralWidget(self.treeWidget)
        self.setWindowTitle("QTreeWidget with Widgets Example")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
