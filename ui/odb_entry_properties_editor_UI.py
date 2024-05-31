import sys
from PySide2 import QtWidgets
from ui.style.icons import OriginIcons
from ui.style import buttons_styles as btns
from common_utils import nice_names as nice_names
from o_database.entities.actions import Query, Set
from envars.origin_envars import OriginEnvar


class EntryPropertiesEditorUI(QtWidgets.QWidget):
    changes_to_database = []

    def __init__(self, parent=None):
        super(EntryPropertiesEditorUI, self).__init__(parent)

        self.create_widget()
        self.create_layout()
        self.create_connections()

    def create_widget(self):
        buttons_style = """
                    QPushButton {
                        border: none;
                        background: transparent;
                    }
                    QPushButton:pressed {
                        background: transparent;
                    }
                    QPushButton:hover {
                        border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
                        background: transparent;
                    }
                """

        self.properties_viewer = QtWidgets.QTableWidget()
        self.properties_viewer.setColumnCount(2)
        self.properties_viewer.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
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

        self.refresh_btn = QtWidgets.QPushButton()
        self.refresh_btn.setIcon(OriginIcons().refresh_button_icon())
        self.refresh_btn.setFixedSize(32, 32)
        self.refresh_btn.setStyleSheet(btns.hover_orange)


        self.commit_btn = QtWidgets.QPushButton()
        self.commit_btn.setIcon(OriginIcons().save_button_icon())
        self.commit_btn.setFixedSize(32, 32)
        self.commit_btn.setStyleSheet(btns.hover_orange)

    def create_layout(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.commit_btn)
        buttons_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.properties_viewer)


    def create_connections(self):
        self.commit_btn.clicked.connect(self.save_properties_to_db)
        self.refresh_btn.clicked.connect(self.populate_properties_list)

    def extract_properties(self):
        data = {}

        for row in range(self.properties_viewer.rowCount()):
            attribute_name = self.properties_viewer.cellWidget(row, 0).text()
            ugly_name = nice_names.write_ugly_names(attribute_name)
            value_text = self.properties_viewer.item(row, 1).text()
            data[ugly_name] = value_text

        return data

    def save_properties_to_db(self):
        data_to_insert = self.extract_properties()
        entity_id = OriginEnvar.entity_id
        Set().entity(entity_id=entity_id).definition = data_to_insert

    def create_properties(self, properties):
        if properties:

            row_count = (len(properties))
            self.properties_viewer.setRowCount(row_count)

            for row, (attr_name, attr_value) in enumerate(properties.items()):
                self.attr_name_le = QtWidgets.QLineEdit()
                self.attr_name_le.setReadOnly(True)
                self.attr_name_le.setMaximumHeight(17)

                attr_nice = nice_names.write_nice_names([attr_name])

                value_item = QtWidgets.QTableWidgetItem(str(attr_value))

                self.attr_name_le.setText(attr_nice[0])

                self.properties_viewer.setCellWidget(row, 0, self.attr_name_le)
                self.properties_viewer.setItem(row, 1, value_item)

    def populate_properties_list(self):
        properties = self.get_entry_properties()
        self.properties_viewer.clear()
        self.create_properties(properties)

    def get_entry_properties(self):
        spare_it = {}
        curr_asset_id = OriginEnvar.entity_id
        curr_asset_type = OriginEnvar.entity_type

        definitions_list = Query().entity(entity_id=curr_asset_id).definition

        if curr_asset_type != "group":
            if definitions_list is None:
                return spare_it
            else:
                try:
                    if len(definitions_list) == 0:
                        return spare_it
                    elif len(definitions_list) >= 1:
                        return definitions_list
                except ValueError as e:
                    raise e
        else:
            return spare_it

    def check_changes(self):
        if len(self.changes_to_database) != 0:
            self.commit_btn.setStyleSheet("background-color: #db70b8; color: black")
        else:
            self.commit_btn.setStyleSheet("QPushButton { border: none; background: transparent; }")

if __name__=="__main__":
    definition = {
        "asset_lod": "hero",
        "assembly": False,
        "full_range_in": "1001",
        "full_range_out": "1100",
        "frame_in": "1001",
        "frame_out": "1100",
        "handles_head": "8",
        "handles_tail": "8",
        "preroll": "10",
        "shot_type": "vfx",
        "cut_in": "1009",
        "cut_out": "993",
        "frame_rate": "24",
        "motion_blur_high": "0.25",
        "motion_blur_low": "-0.25",
        "resolution_width": "1920",
        "resolution_height": "1080"
    }


    app = QtWidgets.QApplication(sys.argv)
    test_dialog = EntryPropertiesEditorUI()
    test_dialog.create_properties(definition)
    test_dialog.show()
    sys.exit(app.exec_())