import sys
from PySide2 import QtWidgets
from origin.envars.origin_envars import ContextHandler
from origin.database.entities.actions import Create


class CreateShowUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateShowUI, self).__init__(parent)

        self.setWindowTitle("Create Show")
        self.setMinimumWidth(250)
        self.setMinimumHeight(150)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLineEdit()
        self.show_code_le = QtWidgets.QLineEdit()
        self.show_type_cb = QtWidgets.QComboBox()
        self.show_type_cb.addItems(["vfx", "commercial"])

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Enter Show Name:", self.show_name_le)
        form_layout.addRow("Enter Show Code:", self.show_code_le)
        form_layout.addRow("Select Show Type:", self.show_type_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        context_handler = ContextHandler()
        context_handler.show_name = self.show_name_le.text()

        db_create = Create(context=context_handler)

        db_create.project(name=self.show_name_le.text(),
                          project_type=self.show_type_cb.currentText(),
                          project_code=self.show_code_le.text())

        assets_id = db_create.group(name="assets", parent=context_handler.show_name)
        sequences_id = db_create.group(name="sequences", parent=context_handler.show_name)
        rnd_seq_id = db_create.group(name="RND", parent=sequences_id)
        rnd_shot_id = db_create.asset(name="0100", parent=rnd_seq_id)
        rnd_shot_breakdown_id = db_create.asset_breakdown(parent_id=rnd_shot_id)

        templates_id = db_create.group(name="templates", parent=context_handler.show_name)
        lists_id = db_create.group(name="Lists", parent=context_handler.show_name)

        references_id = db_create.group(name="references", parent=context_handler.show_name)

        dataops_id = db_create.group(name="data_ops", parent=context_handler.show_name)
        incoming_id = db_create.asset(name="incoming", parent=dataops_id)
        incoming_breakdown_id = db_create.asset_breakdown(parent_id=incoming_id)

        outgoing_id = db_create.asset(name="outgoing", parent=dataops_id)
        outgoing_breakdown_id = db_create.asset_breakdown(parent_id=outgoing_id)

        maya_templates = db_create.group(name="maya", parent=templates_id)
        gaffer_templates = db_create.group(name="gaffer", parent=templates_id)
        nuke_templates = db_create.group(name="nuke", parent=templates_id)
        video_templates = db_create.group(name="video", parent=templates_id)

        maya_playblast_id = db_create.asset(name="playblast", parent=maya_templates)
        maya_playblast_breakdown = db_create.asset_breakdown(parent_id=maya_playblast_id)
        playblast_task = db_create.task(name="template", parent=maya_playblast_id, task_type="template")

        characters_cat_id = db_create.group(name="characters", parent=assets_id)
        props_cat_id = db_create.group(name="props", parent=assets_id)
        environments_cat_id = db_create.group(name="environments", parent=assets_id)
        vehicles_cat_id = db_create.group(name="vehicles", parent=assets_id)


        self.show_name_le.clear()
        self.show_code_le.clear()


if __name__ == "__main__":
    from origin.ui.tests.manual_cotext import test_ui

    test_ui(main_widget=CreateShowUI)

