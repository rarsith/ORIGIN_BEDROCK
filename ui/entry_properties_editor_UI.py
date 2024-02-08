import sys
from PySide2 import QtWidgets
from common_utils import nice_names as nice_names


class EntryPropertiesEditorUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EntryPropertiesEditorUI, self).__init__(parent)

        self.create_widget()
        self.create_layout()

    def create_widget(self):
        self.properties_viewer = QtWidgets.QTableWidget()
        self.properties_viewer.setColumnCount(2)
        self.properties_viewer.setColumnWidth(0, 250)
        self.properties_viewer.setColumnWidth(1, 120)

        self.properties_viewer.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.properties_viewer.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.properties_viewer.verticalScrollBar().setVisible(False)
        self.properties_viewer.horizontalScrollBar().setVisible(False)

        self.properties_viewer.setShowGrid(False)
        vertical_header = self.properties_viewer.verticalHeader()

        for row in range(self.properties_viewer.rowCount()):
            self.properties_viewer.setRowHeight(row, 10)

        self.properties_viewer.setAlternatingRowColors(False)

        header = self.properties_viewer.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        vertical_header.setDefaultSectionSize(2)
        vertical_header.hide()
        horizontal_header = self.properties_viewer.horizontalHeader()
        horizontal_header.setMinimumHeight(2)
        horizontal_header.setMaximumHeight(3)
        horizontal_header.hide()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.properties_viewer)

    def create_properties(self, properties):
        try:
            self.properties_viewer.setRowCount(0)
            store_attributes_names = (list(properties.keys()))
            write_attrib_nice = nice_names.write_nice_names(store_attributes_names)

            for i in range(len(store_attributes_names)):
                get_properties_names = write_attrib_nice[i]
                get_properties_values = list(properties.values())[i]
                self.properties_viewer.insertRow(i)
                self.insert_item(i, 0, str(get_properties_names))
                self.insert_item(i, 1, str(get_properties_values))
        except:
            pass

    def insert_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        self.properties_viewer.setItem(row, column, item)


if __name__=="__main__":
    definition = {
        "asset_lod": "hero",
        "assembly": False,
        "full_range_in": "1001",
        "full_range_out": "1100",
        "frame_in": "1001",
        "frame_out": "1001",
        "handles_head": "8",
        "handles_tail": "8",
        "preroll": "10",
        "shot_type": "vfx",
        "cut_in": "1009",
        "cut_out": "993",
        "frame_rate": "24",
        "motion_blur_high": "0.25",
        "motion_blur_low": "-0.25",
        "res_x": "from plate",
        "res_y": "from plate"
    }


    app = QtWidgets.QApplication(sys.argv)
    test_dialog = EntryPropertiesEditorUI()
    test_dialog.create_properties(definition)
    test_dialog.show()
    sys.exit(app.exec_())