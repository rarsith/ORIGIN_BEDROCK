import sys
from PySide2 import QtWidgets



class SlotComponentsViewerBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(SlotComponentsViewerBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setColumnCount(3)
        self.setRowCount(1)
        self.setShowGrid(False)

        # self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 250)
        self.setColumnWidth(2, 60)

        self.setMinimumWidth(600)
        self.setSortingEnabled(True)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 20)

        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)

        vertical_header = self.verticalHeader()
        vertical_header.hide()
        horizontal_header = self.horizontalHeader()
        horizontal_header.hide()
        horizontal_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


class SlotComponentsViewerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SlotComponentsViewerUI, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.slot_component_viewer_tw = SlotComponentsViewerBuild()

    def create_layout(self):
        slot_view_layout = QtWidgets.QVBoxLayout()
        slot_view_layout.addWidget(self.slot_component_viewer_tw)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(slot_view_layout)



if __name__ == "__main__":
    import pprint
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = SlotComponentsViewerUI()
    test_dialog.show()
    sys.exit(app.exec_())