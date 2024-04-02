
from PySide2 import QtWidgets
from o_database.odb_statuses import DbTaskStatuses

class TaskStatusWidget(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(TaskStatusWidget, self).__init__(parent)

        self.addItems(DbTaskStatuses().list_all())

        self.setStyleSheet(f"""
        QComboBox:item:selected[text={DbTaskStatuses().wip}] {{color:yellow:}}
        """)

