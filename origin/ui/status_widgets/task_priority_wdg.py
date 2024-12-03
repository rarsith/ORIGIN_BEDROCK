
from PySide2 import QtWidgets
from origin.database.priorities import DbPriorities
from origin.ui.status_widgets.color_settings import match_color_scheme


class TaskPriorityWidget(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(TaskPriorityWidget, self).__init__(parent)
        self.wheelEvent = lambda event: None
        self.addItems(DbPriorities().list_all())

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