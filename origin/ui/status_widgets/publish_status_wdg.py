
from PySide2 import QtWidgets, QtCore, QtGui
from origin.database.statuses import DbVersionStatuses


class CustomDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Set the color based on the index or any other criteria
        if index.row() % 2 == 0:
            color = QtGui.QColor(QtCore.Qt.green)
        else:
            color = QtGui.QColor(QtCore.Qt.blue)

        # Paint the background with the desired color
        painter.fillRect(option.rect, color)

        # Draw the item text
        painter.drawText(option.rect, QtCore.Qt.AlignCenter, index.data())


class PublishStatusWidget(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(PublishStatusWidget, self).__init__(parent)
        self.wheelEvent = lambda event: None
        self.addItems(DbVersionStatuses().list_all())

        self.currentIndexChanged.connect(self.updateStyle)

        self.updateStyle(0)

    def updateStyle(self, index):
        current_text = self.itemText(index)
        if current_text == "WIP":
            self.setStyleSheet("background-color: #BBCB0F; color: black")

        elif current_text == "IN PROGRESS":
            self.setStyleSheet("background-color: #80ccff; color: black")

        elif current_text == "PENDING REVIEW":
            self.setStyleSheet("background-color: #ffc266; color: black")

        elif current_text == "TWEAK":
            self.setStyleSheet("background-color: #db70b8; color: black")

        elif current_text == "IGNORE":
            self.setStyleSheet("background-color: #bfbfbf; color: #595959")

        elif current_text == "REJECTED":
            self.setStyleSheet("background-color: #c86851; color: #d9d9d9")

        elif current_text == "INTERNAL APPROVED":
            self.setStyleSheet("background-color: #99cc00; color: #404040")

        elif current_text == "CLIENT APPROVED":
            self.setStyleSheet("background-color: #00802b; color: #333333")

        elif current_text == "READY TO DELIVER":
            self.setStyleSheet("background-color: #00802b; color: #333333")

        elif current_text == "TEMP APPROVED":
            self.setStyleSheet("background-color: #e6e600; color: #0d0d0d")

        else:
            self.setStyleSheet("background-color: lightgrey;")



if __name__ == "__main__":
    wip: str = "WIP"
    init: str = "READY TO START"
    in_progress: str = "IN PROGRESS"
    completed: str = "COMPLETED"
    omitted: str = "OMITTED"
    on_hold: str = "ON HOLD"