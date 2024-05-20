import sys
from PySide2 import QtWidgets, QtCore, QtGui


class PublishSlotsWidgetBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PublishSlotsWidgetBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setDisabled(False)
        self.setMinimumWidth(690)
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels(["Slot", "Type", "Method", "Source", "Scope", "Mode", "Artists","R", "A"])
        self.setShowGrid(False)
        self.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.setAlternatingRowColors(True)
        header = self.verticalHeader()
        header.hide()
        self.setColumnWidth(0, 110)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 90)
        self.setColumnWidth(3, 110)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 75)
        self.setColumnWidth(6, 90)
        self.setColumnWidth(7, 20)
        self.setColumnWidth(8, 20)
        self.resizeRowsToContents()


class TaskPubSlotUsedByBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(TaskPubSlotUsedByBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setAlternatingRowColors(False)
        self.setHeaderLabels(['task name'])
        self.setMinimumWidth(160)
        self.setMaximumWidth(170)
        self.setMinimumHeight(300)
        self.setColumnWidth(0, 130)


class PublishSlotsWidgetUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PublishSlotsWidgetUI, self).__init__(parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.tasks_pub_slots_properties_lb = QtWidgets.QLabel("Publishing Slots")
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.tasks_pub_slots_properties_lb.setText("--select a task--")
        self.tasks_pub_slots_properties_lb.setStyleSheet("color: red")
        self.tasks_pub_slots_properties_lb.setFont(my_font)

        self.all_pub_slots_lb = QtWidgets.QLabel()
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.all_pub_slots_lb.setText("--select slot--")
        self.all_pub_slots_lb.setStyleSheet("color: red")
        self.all_pub_slots_lb.setFont(my_font)


        self.add_pub_slot_le = QtWidgets.QLineEdit()
        self.add_pub_slot_le.setPlaceholderText('New Slot Name!')
        self.add_pub_slot_btn = QtWidgets.QPushButton('Add')

        self.publish_slots_wdg = PublishSlotsWidgetBuild()
        self.dependent_pub_slots_wdg = TaskPubSlotUsedByBuild()

        self.delete_list_item_btn = QtWidgets.QPushButton("Remove Selected")
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.add_pub_slot_le)
        top_layout.addWidget(self.add_pub_slot_btn)

        dependents_layout = QtWidgets.QVBoxLayout()
        dependents_layout.addWidget(self.all_pub_slots_lb)
        dependents_layout.addWidget(self.dependent_pub_slots_wdg)

        publish_slots_layout = QtWidgets.QVBoxLayout()
        publish_slots_layout.addWidget(self.tasks_pub_slots_properties_lb)
        publish_slots_layout.addLayout(top_layout)
        publish_slots_layout.addWidget(self.publish_slots_wdg)

        pub_and_dep_layout = QtWidgets.QHBoxLayout()
        pub_and_dep_layout.addLayout(publish_slots_layout)
        pub_and_dep_layout.addLayout(dependents_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(pub_and_dep_layout)
        main_layout.addWidget(self.delete_list_item_btn)
        main_layout.addWidget(self.save_btn)
        main_layout.addWidget(self.refresh_btn)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = PublishSlotsWidgetUI()
    test_dialog.show()
    sys.exit(app.exec_())