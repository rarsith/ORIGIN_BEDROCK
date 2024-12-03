from PySide2 import QtWidgets, QtCore, QtGui
from origin.database.statuses import DbTaskStatuses
from origin.ui.status_widgets.color_settings import match_color_scheme


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
        get_color_schema = match_color_scheme(current_text)
        self.setStyleSheet(get_color_schema)


if __name__ == "__main__":
    wip: str = "WIP"
    init: str = "READY TO START"
    in_progress: str = "IN PROGRESS"
    completed: str = "COMPLETED"
    omitted: str = "OMITTED"
    on_hold: str = "ON HOLD"
