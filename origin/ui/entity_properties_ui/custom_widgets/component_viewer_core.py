import sys
from pathlib import Path

from PySide2 import QtWidgets, QtGui, QtCore

from origin.envars.Xorigin_envars import ContextHandler
from origin.o_database.entities.Xoperators import CollectionOperators
from origin.ui.entity_properties_ui.custom_widgets.component_viewer_UI import SlotComponentsViewerUI

img_path = "/Users/arsithra/Documents/Learning_Python/PycharmProjects/Xchange/xcg_icons/play_icon_vsmall.png"


class SetReviewableComponent(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(SetReviewableComponent, self).__init__(parent)
        pic_video = QtGui.QPixmap(img_path)
        self.setIcon(pic_video)


class ComponentViewerWidget(QtWidgets.QWidget):
    def __init__(self, label: str, file_path: str, parent=None):
        super(ComponentViewerWidget, self).__init__(parent)

        self.label = label
        self.file_path = file_path

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.component_name_lb = QtWidgets.QLabel("component_name")
        self.component_name_lb.setText(self.label)
        self.component_name_lb.setMinimumWidth(75)
        self.component_name_lb.setAlignment(QtCore.Qt.AlignCenter)

        self.path_le = QtWidgets.QLineEdit("Some text")
        self.path_le.setReadOnly(True)
        self.path_le.setText(self.file_path)
        self.path_le.setCursorPosition(0)

        self.copy_path_btn = QtWidgets.QPushButton("Copy Path")
        self.copy_path_btn.setMinimumWidth(60)

        self.open_with_btn = QtWidgets.QPushButton("Open With...")
        self.open_with_btn.setMinimumWidth(50)
        # self.open_with_btn.setFixedSize(50, 15)

        self.proc_progress_bar = QtWidgets.QProgressBar()
        self.proc_progress_bar.setValue(100)
        self.proc_progress_bar.setFixedHeight(10)

        self.pub_status_lb = QtWidgets.QLabel("---")
        self.pub_status_lb.setMinimumWidth(50)
        self.pub_status_lb.setAlignment(QtCore.Qt.AlignCenter)

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.component_name_lb)
        top_layout.addWidget(self.pub_status_lb)
        top_layout.addStretch(1)
        top_layout.addWidget(self.copy_path_btn)
        top_layout.addWidget(self.open_with_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(1)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.path_le)
        # main_layout.addWidget(self.proc_progress_bar)

    def create_connections(self):
        self.copy_path_btn.clicked.connect(self.copy_to_clipboard)

    def copy_to_clipboard(self):
        unix_style_path = Path(self.path_le.text())
        if QtCore.QSysInfo().productType() == 'windows':
            os_compatible_path = unix_style_path.__str__()
        else:
            os_compatible_path = unix_style_path.as_posix()
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(os_compatible_path)


class SlotComponentsViewerCore(SlotComponentsViewerUI):

    def __init__(self, parent=None):
        super(SlotComponentsViewerCore, self).__init__(parent)

        self.context_handler = None

    def get_selection_id(self):
        if self.slot_component_viewer_tw.selectedItems():
            cell_name = self.slot_component_viewer_tw.selectedItems()[6]
            return cell_name.text()

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context

    def populate_widget(self):
        db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        file_comp_docs = db_ops.entities_attr_value_starts_with(attr_field="_id",
                                                                val_starts_with=self.context_handler.db_asset_version_id,
                                                                extra_filters=[{"type": "db_asset_file_component"}])
        self.slot_component_viewer_tw.clear()
        row_count = (len(file_comp_docs))
        self.slot_component_viewer_tw.setRowCount(row_count)

        cnt = 1
        if file_comp_docs:
            reserved_doc = None
            for doc in file_comp_docs:
                if doc['label'] == "origin_scene":
                    reserved_doc = doc
                    file_comp_docs.remove(doc)

            for file_comp_doc in file_comp_docs:
                self.compile_file_component_widget(
                    label=file_comp_doc['label'],
                    file_path=file_comp_doc["file_path"],
                    row=cnt)

                cnt += 1
            if reserved_doc:
                self.compile_file_component_widget(
                    label=reserved_doc['label'],
                    file_path=reserved_doc["file_path"],
                    row=0)

    def compile_file_component_widget(self, label, file_path, row):
        components_widget = ComponentViewerWidget(label=label, file_path=file_path)
        self.slot_component_viewer_tw.setCellWidget(row, 0, components_widget)
        self.slot_component_viewer_tw.setRowHeight(row, 80)


if __name__ == "__main__":
    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'yellow_hulk',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.yellow_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "New_State.assets.chr.yellow_hulk.modeling",
                      'db_asset_id': 'New_State.assets.chr.yellow_hulk.modeling.foo'}

    context_class = ContextHandler()
    context_class.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = ComponentViewerWidget()

    test_dialog.show()
    sys.exit(app.exec_())
