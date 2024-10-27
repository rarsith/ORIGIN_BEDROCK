
from PySide2 import QtWidgets
from origin.database.priorities import DbPriorities

class TaskPriorityWidget(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(TaskPriorityWidget, self).__init__(parent)
        self.wheelEvent = lambda event: None
        self.addItems(DbPriorities().list_all())

        self.currentIndexChanged.connect(self.updateStyle)

        self.updateStyle(0)

    def updateStyle(self, index):
        current_text = self.itemText(index)
        if current_text == "LOW":
            self.setStyleSheet("background-color: #ADC01E; color: black")
        elif current_text == "MEDIUM":
            self.setStyleSheet("background-color: #20A8C9; color: black")
        elif current_text == "HIGH":
            self.setStyleSheet("background-color: #C12020; color: black")
        elif current_text == "NORMAL":
            self.setStyleSheet("background-color: #8D8D8D; color: black")
        elif current_text == "CRITICAL":
            self.setStyleSheet("background-color: #880000; color: #FFFFFF")

        else:
            self.setStyleSheet("background-color: lightgrey;")

if __name__ == "__main__":
    wip: str = "WIP"
    init: str = "READY TO START"
    in_progress: str = "IN PROGRESS"
    completed: str = "COMPLETED"
    omitted: str = "OMITTED"
    on_hold: str = "ON HOLD"