import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QDateEdit, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import QDate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        layout = QVBoxLayout(self.centralWidget)

        self.treeWidget = QTreeWidget()
        layout.addWidget(self.treeWidget)

        self.treeWidget.setHeaderLabels(["Column 1", "Column 2"])

        # Inserting items with QDateEdit in the second column
        for i in range(5):
            item = QTreeWidgetItem(["Item {}".format(i)])
            self.treeWidget.addTopLevelItem(item)

            date_edit = QDateEdit()
            date_edit.setDate(QDate.currentDate())  # Set current date as default
            self.treeWidget.setItemWidget(item, 1, date_edit)  # Add QDateEdit to second column

            # Connect the dateChanged signal of QDateEdit to a slot
            date_edit.dateChanged.connect(lambda date, row=i: self.date_changed_slot(date, row))

    def date_changed_slot(self, date, row):
        print("Date changed in row", row, ":", date.toString("yyyy-MM-dd"))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
