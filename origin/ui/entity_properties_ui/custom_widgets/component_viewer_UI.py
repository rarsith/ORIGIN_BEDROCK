import sys
from PySide2 import QtWidgets, QtCore
from origin.ui.style.icons import OriginIcons
from origin.ui.style import buttons_styles as btns


class SlotComponentsViewerBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(SlotComponentsViewerBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setColumnCount(2)
        # self.setRowCount(0)
        self.setShowGrid(False)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setColumnWidth(0, 450)

        self.setSortingEnabled(True)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 200)

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
        self.play_btn = QtWidgets.QPushButton()
        self.play_btn.setIcon(OriginIcons().play_icon())
        self.play_btn.setFixedSize(32, 32)
        self.play_btn.setStyleSheet(btns.hover_orange)

        self.open_in_cb = QtWidgets.QPushButton("...")
        self.open_in_cb.setIcon(OriginIcons().play_icon())
        self.open_in_cb.setFixedSize(32, 32)
        self.open_in_cb.setStyleSheet(btns.hover_orange)

    def create_layout(self):
        top_buttons_layout = QtWidgets.QHBoxLayout()
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(self.play_btn)
        top_buttons_layout.addWidget(self.open_in_cb)

        slot_view_layout = QtWidgets.QVBoxLayout()
        slot_view_layout.addWidget(self.slot_component_viewer_tw)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_buttons_layout)
        main_layout.addLayout(slot_view_layout)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = SlotComponentsViewerUI()
    test_dialog.show()
    sys.exit(app.exec_())