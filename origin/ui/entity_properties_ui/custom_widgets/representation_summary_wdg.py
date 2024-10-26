from PySide2 import QtWidgets

from origin.o_database.odb_statuses import DbTaskStatuses


class EntitySummaryInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EntitySummaryInfo, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.status_lb = QtWidgets.QLabel("Status")
        self.status_cb = QtWidgets.QComboBox()
        self.status_cb.addItems(DbTaskStatuses().list_all())

        self.linked_to_lb = QtWidgets.QLabel("Linked to")
        self.task_lb = QtWidgets.QLabel("Task")

    def create_layout(self):
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.status_lb, 0, 0)
        main_layout.addWidget(self.status_cb, 0, 1)
        main_layout.addWidget(self.linked_to_lb, 1, 0)
        main_layout.addWidget(self.task_lb, 2, 0)
