import os

from PySide2 import QtWidgets, QtCore, QtGui

from origin.paths.output_paths import OriginOSPathHandler
from origin.ui.loaders_ui.color_settings import match_icon_status_scheme
from origin.common_utils import nice_names
from origin.database.mongo import CollectionOperators
from origin.envars.origin_envars import ContextHandler


class EntityPropertiesInfo(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(EntityPropertiesInfo, self).__init__(parent)

        self.setColumnCount(2)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)

        self.setFocusPolicy(QtCore.Qt.NoFocus)  # Prevent focus-based highlight
        self.setSelectionMode(QtWidgets.QTableWidget.NoSelection)

        self.setMaximumHeight(150)

        # self.setShowGrid(False)
        vertical_header = self.verticalHeader()

        for row in range(self.rowCount()):
            self.setRowHeight(row, 10)

        # self.setAlternatingRowColors(True)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        vertical_header.setDefaultSectionSize(2)
        vertical_header.hide()

        horizontal_header = self.horizontalHeader()
        horizontal_header.setMinimumHeight(2)
        horizontal_header.setMaximumHeight(3)
        horizontal_header.hide()


class PlayblastOptionsUI(QtWidgets.QDialog):
    def __init__(self, context: ContextHandler, dcc=None, parent=None):
        super(PlayblastOptionsUI, self).__init__(parent)

        self.dcc = os.getenv("DCC")

        if dcc is not None:
            self.dcc = dcc
        else:
            self.dcc = "maya"

        self.context_handler = context

        self.path_manager = OriginOSPathHandler(context=self.context_handler)

        self.id_root = ".".join([self.context_handler.show_name,
                                 "templates",
                                 self.dcc,
                                 "playblast"
                                 ])
        print ( "ID ROOT:  ", self.id_root )

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.populate_properties_list()
        self.populate_frame_ranges()
        self.populate_render_resolutions()
        self.populate_render_percentage()
        self.populate_template_streams()
        self.populate_template_versions()
        self.populate_camera_versions()

    def reinitialize(self, pub_options=None):
        pass

    def create_widgets(self):
        stream_name = ''
        if self.context_handler.db_asset_stream_id is not None:
            if "." in self.context_handler.db_asset_stream_id:
                stream_name = self.context_handler.db_asset_stream_id.rsplit(".", 1)[1]

        title_name = f"Current Properties for --> {self.context_handler.entity_name.capitalize()} --> {stream_name}"

        self.entity_info_lb = QtWidgets.QLabel(title_name)
        self.entity_properties_info_tw = EntityPropertiesInfo()

        self.frame_range_cb = QtWidgets.QComboBox()
        self.frame_range_cb.setMinimumWidth(300)

        self.frame_step_cb = QtWidgets.QComboBox()
        self.frame_step_cb.setMinimumWidth(300)

        self.template_streams_cb = QtWidgets.QComboBox()
        self.template_streams_cb.setMinimumWidth(300)

        self.template_select_cb = QtWidgets.QComboBox()
        self.template_select_cb.setMinimumWidth(300)

        self.resolution_cb = QtWidgets.QComboBox()
        self.resolution_cb.setMinimumWidth(300)

        self.resolution_procentage_cb = QtWidgets.QComboBox()
        self.resolution_procentage_cb.setMinimumWidth(300)

        self.active_camera_cb = QtWidgets.QComboBox()
        self.active_camera_cb.setMinimumWidth(300)

        self.playblast_btn = QtWidgets.QPushButton("Playblast")
        self.cancel_bn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        entity_info_layout = QtWidgets.QVBoxLayout()
        entity_info_layout.addWidget(self.entity_info_lb)
        entity_info_layout.addWidget(self.entity_properties_info_tw)

        options_layout = QtWidgets.QFormLayout()
        options_layout.addRow("Frame Range", self.frame_range_cb)
        options_layout.addRow("Frame Step", self.frame_step_cb)
        options_layout.addRow("Resolution", self.resolution_cb)
        options_layout.addRow("Resolution Percentage", self.resolution_procentage_cb)
        options_layout.addRow("Template Streams", self.template_streams_cb)
        options_layout.addRow("Template Version", self.template_select_cb)
        options_layout.addRow("Camera Version", self.active_camera_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.cancel_bn)
        buttons_layout.addWidget(self.playblast_btn)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(entity_info_layout)
        self.main_layout.addLayout(options_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)

    def create_properties(self, properties):
        attr_to_extract = ["frame_in", "frame_out", "preroll", "cut_in", "cut_out", "handles_head", "handles_tail"]

        if properties:

            row_count = (len(attr_to_extract))
            self.entity_properties_info_tw.setRowCount(row_count)

            for row, attr in enumerate(attr_to_extract):
                self.attr_name_le = QtWidgets.QLineEdit()
                self.attr_name_le.setReadOnly(True)
                self.attr_name_le.setMaximumHeight(17)

                attr_nice = nice_names.write_nice_names([attr])

                value_item = QtWidgets.QTableWidgetItem(str(properties[attr]))
                value_item.setFlags(value_item.flags() & ~QtCore.Qt.ItemIsEditable)
                value_item.setFlags(value_item.flags() & ~QtCore.Qt.ItemIsSelectable)

                self.attr_name_le.setText(attr_nice[0])

                self.entity_properties_info_tw.setCellWidget(row, 0, self.attr_name_le)
                self.entity_properties_info_tw.setItem(row, 1, value_item)

    def populate_properties_list(self):
        properties = self.get_entity_properties()
        self.entity_properties_info_tw.clear()
        self.create_properties(properties)

    def get_entity_properties(self):
        entity_doc = self.context_handler.database_handler().get_asset_document()
        entity_properties = entity_doc.definition
        return entity_properties

    def create_connections(self):
        self.playblast_btn.clicked.connect(self.get_selected_options)
        self.template_streams_cb.currentIndexChanged.connect(self.populate_template_versions)

    def populate_frame_ranges(self):
        self.frame_range_cb.clear()
        frame_ranges = self.get_frame_ranges()
        for fr_range in frame_ranges:
            for range_name, range_value in fr_range.items():
                self.frame_range_cb.addItem(range_name + " --> " + str(range_value), userData=range_value)

    def get_frame_ranges(self):
        frame_ranges = []
        entity_properties = self.get_entity_properties()

        work_range = {"work_range": (int(entity_properties["frame_in"]), int((entity_properties["frame_out"])) + 1)}
        frame_ranges.append(work_range)

        include_preroll = (int(entity_properties["frame_in"]) - int(entity_properties["preroll"])) - 1
        with_preroll_range = {"with_preroll": (include_preroll, int(entity_properties["frame_out"]) + 1)}
        frame_ranges.append(with_preroll_range)

        cut_range = {"cut_range": (int(entity_properties["frame_in"]) + int(entity_properties["handles_head"]),
                                   int(entity_properties["frame_out"]) - int(entity_properties["handles_tail"]))}

        frame_ranges.append(cut_range)

        return frame_ranges

    def populate_render_percentage(self):
        procentages = {"100%": 1, "75%": 0.75, "50%": 0.5}

        for proc, value in procentages.items():
            self.resolution_procentage_cb.addItem(proc, userData=value)

    def populate_render_resolutions(self):
        entity_properties = self.get_entity_properties()
        resolution_display = f"{str(entity_properties['res_x'])} x {str(entity_properties['res_y'])}"

        resolution = {resolution_display: (entity_properties['res_x'], entity_properties['res_y'])}

        self.resolution_cb.addItem(resolution_display, userData=resolution[resolution_display])


    def populate_template_streams(self):
        self.template_streams_cb.clear()

        stored_streams = self.get_template_streams()
        if stored_streams is not None:
            for stream in stored_streams:
                stream_name = stream.rsplit(".", 1)[1]
                self.template_streams_cb.addItem(stream_name, userData=stream)

    def update_template_to_status(self):
        pass

    def populate_template_versions(self):
        self.template_select_cb.clear()

        current_sel_stream = self.template_streams_cb.currentData()
        fetch_ent = CollectionOperators(db_collection=self.context_handler.project_publishes)
        get_sel_stream_doc = fetch_ent.entity_document(doc_id=current_sel_stream)

        get_all_versions = None
        allowed_statuses = ["INTERNAL APPROVED", "WIP", "PENDING REVIEW"]

        if get_sel_stream_doc:
            get_task_db_asset_id = get_sel_stream_doc['children'][0]

            extra_filters = [{"status": allowed_statuses}]

            get_all_versions = fetch_ent.entities_attr_value_starts_with(attr_field="_id",
                                                                         val_starts_with=get_task_db_asset_id,
                                                                         extra_filters=extra_filters
                                                                         )
        # model = QtGui.QStandardItemModel()
        # item = QtGui.QStandardItem(display_name)
        # item.setBackground(QtGui.QColor())
        if get_all_versions:
            for version in get_all_versions:
                display_name = ".".join(version["_id"].rsplit(".")[-3:])
                get_status_style = match_icon_status_scheme(version["status"])
                template_ver_file_component = fetch_ent.entities_attr_value_starts_with(attr_field="parent",
                                                                                        val_starts_with=version["_id"],
                                                                                        extra_filters=[
                                                                                            {"file_extension": "master"}
                                                                                        ]
                                                                                        )

                file_rel_path = template_ver_file_component[0]["file_path"]
                resolve_path = self.path_manager.resolve_to_absolute_path(file_rel_path)
                unix_path = self.path_manager.convert_path_to_unix(resolve_path)
                self.template_select_cb.addItem(QtGui.QIcon(get_status_style), display_name, userData=unix_path)

            to_select_index = []
            for status in allowed_statuses:
                for idx, version in enumerate(get_all_versions):
                    if len(to_select_index) == 0:
                        if version["status"] == status:
                            to_select_index.append(idx)
                            break
                    else:
                        break

            self.template_select_cb.setCurrentIndex(to_select_index[0])

    def populate_camera_versions(self):
        self.active_camera_cb.clear()
        fetch_ent = CollectionOperators(db_collection=self.context_handler.project_publishes)

        camera_parent_id = ".".join([self.context_handler.entity_id, "turntable_camera"])

        allowed_statuses = ["INTERNAL APPROVED", "WIP", "PENDING REVIEW"]
        extra_filters = [{"status": allowed_statuses}]
        get_all_versions = fetch_ent.entities_attr_value_starts_with(attr_field="parent",
                                                                     val_starts_with=camera_parent_id,
                                                                     extra_filters=extra_filters
                                                                     )

        to_select_index = []
        if get_all_versions:
            for version in get_all_versions:
                display_name = ".".join(version["_id"].rsplit(".")[-3:])
                get_status_style = match_icon_status_scheme(version["status"])
                cam_ver_file_component = fetch_ent.entities_attr_value_starts_with(attr_field="parent",
                                                                                   val_starts_with=version["_id"],
                                                                                   extra_filters=[
                                                                                       {"file_extension": "abc"}
                                                                                   ]
                                                                                   )

                if cam_ver_file_component:
                    file_rel_path = cam_ver_file_component[0]["file_path"]
                    resolve_path = self.path_manager.resolve_to_absolute_path(file_rel_path)
                    unix_path = self.path_manager.convert_path_to_unix(resolve_path)
                    self.active_camera_cb.addItem(QtGui.QIcon(get_status_style), display_name, userData=unix_path)

            for status in allowed_statuses:
                for idx, version in enumerate(get_all_versions):
                    if len(to_select_index) == 0:
                        if version["status"] == status:
                            to_select_index.append(idx)
                            break
                    else:
                        break

            self.active_camera_cb.setCurrentIndex(to_select_index[0])

    def get_template_streams(self):
        fetch_ent = CollectionOperators(db_collection=self.context_handler.show_name)
        template_entity = fetch_ent.entity_document(doc_id=self.id_root)
        template_streams = template_entity["stack_streams"]

        return template_streams

    def get_selected_options(self):
        options = {"frame_range": self.frame_range_cb.currentData(),
                   "resolution": self.resolution_cb.currentData(),
                   "resolution_percentage": self.resolution_procentage_cb.currentData(),
                   "template_asset_ver_id": self.template_select_cb.currentData(),
                   "camera_asset_ver_id": self.active_camera_cb.currentData()}

        return {"review_options": options}


if __name__ == "__main__":
    import sys
    from origin.ui.tests.manual_cotext import test_ui

    app, ui = test_ui(main_widget=PlayblastOptionsUI, run_app=False, dcc="maya")

    sys.exit(app.exec_())
