from PySide2.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QApplication, QComboBox
from PySide2 import QtCore, QtWidgets
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt


class CustomDelegateQTree(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size_hint = super().sizeHint(option, index)
        size_hint.setHeight(40)  # Set the desired row height here
        return size_hint


class CustomTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setItemDelegate(CustomDelegate())
        self.setColumnCount(1)

        for i in range(10):
            item = QTreeWidgetItem(self)
            item.setText(0, "Item {}".format(i))


def main():
    app = QApplication([])
    treeWidget = CustomTreeWidget()
    treeWidget.show()
    app.exec_()


class CustomDelegate(QStyledItemDelegate):

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.showDecorationSelected = False

    def paint(self, painter, option, index):
        painter.save()
        if option.state & QtWidgets.QStyle.State_Selected:
            option.state ^= QtWidgets.QStyle.State_Selected
        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, index.data())
        painter.restore()

class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                    QComboBox::item:selected {
                        background-color: transparent;
                    }
                """)


        self.setItemDelegate(CustomDelegate())
        self.addItems(["approved", "WIP", "Ignore"])
        self.currentIndexChanged.connect(self.updateStyle)

    def updateStyle(self, index):
        current_text = self.itemText(index)
        if current_text == "approved":
            self.setStyleSheet("background-color: green;")
        elif current_text == "WIP":
            self.setStyleSheet("background-color: blue;")
        elif current_text == "Ignore":
            self.setStyleSheet("background-color: gray;")
        else:
            self.setStyleSheet("background-color: white;")

def main():
    app = QApplication([])
    comboBox = CustomComboBox()
    comboBox.show()
    app.exec_()



if __name__ == "__main__":
    main()


