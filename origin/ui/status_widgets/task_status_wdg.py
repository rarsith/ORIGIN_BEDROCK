
from PySide2 import QtWidgets, QtCore, QtGui
from origin.database.statuses import DbTaskStatuses


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


class TaskStatusWidget(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(TaskStatusWidget, self).__init__(parent)
        self.wheelEvent = lambda event: None
        self.addItems(DbTaskStatuses().list_all())

        self.currentIndexChanged.connect(self.updateStyle)

        self.updateStyle(0)

    def updateStyle(self, index):
        current_text = self.itemText(index)
        if current_text == "WIP":
            self.setStyleSheet("background-color: #BBCB0F; color: black")
        elif current_text == "READY TO START":
            self.setStyleSheet("background-color: #6C89BF;")
        elif current_text == "IN PROGRESS":
            self.setStyleSheet("background-color: #5EBEA6; color: black")
        elif current_text == "COMPLETED":
            self.setStyleSheet("background-color: #1F8918; color: black")
        elif current_text == "OMITTED":
            self.setStyleSheet("background-color: #936E94; color: black")
        elif current_text == "ON HOLD":
            self.setStyleSheet("background-color: #A41A1A; color: black")
        elif current_text == "NOT STARTED":
            self.setStyleSheet("background-color: #636363; color: #A8A8A8")

        else:
            self.setStyleSheet("background-color: lightgrey;")



if __name__ == "__main__":
    wip: str = "WIP"
    init: str = "READY TO START"
    in_progress: str = "IN PROGRESS"
    completed: str = "COMPLETED"
    omitted: str = "OMITTED"
    on_hold: str = "ON HOLD"