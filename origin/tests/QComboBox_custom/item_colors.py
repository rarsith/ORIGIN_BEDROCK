from PySide2.QtWidgets import QApplication, QComboBox, QStyledItemDelegate
from PySide2.QtGui import QColor, QPainter
from PySide2.QtCore import Qt

class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Set the color based on the index or any other criteria
        if index.row() % 2 == 0:
            color = QColor(Qt.green)
        else:
            color = QColor(Qt.blue)

        # Paint the background with the desired color
        painter.fillRect(option.rect, color)

        # Draw the item text
        painter.drawText(option.rect, Qt.AlignCenter, index.data())

class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        delegate = CustomDelegate(self)
        self.setItemDelegate(delegate)

# Example usage:
app = QApplication([])
combo = CustomComboBox()
combo.addItems(["Item 1", "Item 2", "Item 3", "Item 4"])
combo.show()
app.exec_()
