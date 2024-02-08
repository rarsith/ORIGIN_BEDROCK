from PySide2 import QtWidgets


class EntityPropertiesWidgetBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(EntityPropertiesWidgetBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setColumnCount(2)

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)

        self.setShowGrid(False)
        vertical_header = self.verticalHeader()

        for row in range(self.rowCount()):
            self.setRowHeight(row, 10)

        self.setAlternatingRowColors(True)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        vertical_header.setDefaultSectionSize(2)
        vertical_header.hide()
        horizontal_header = self.horizontalHeader()
        horizontal_header.setMinimumHeight(2)
        horizontal_header.setMaximumHeight(3)
        horizontal_header.hide()


class EntityPropertiesUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EntityPropertiesUI, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.properties_viewer_wdg = EntityPropertiesWidgetBuild()

        self.add_prop_le = QtWidgets.QLineEdit()
        self.add_prop_le.setPlaceholderText('New Property Name!')

        self.add_pub_slot_btn = QtWidgets.QPushButton('Add')

        self.rem_sel_item_btn = QtWidgets.QPushButton("Remove Selected")
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")


    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.add_prop_le)
        top_layout.addWidget(self.add_pub_slot_btn)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.properties_viewer_wdg)
        layout.addWidget(self.rem_sel_item_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(layout)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = EntityPropertiesUI()
    test_dialog.show()
    sys.exit(app.exec_())