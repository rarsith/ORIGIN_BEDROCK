import sys
from PySide2 import QtWidgets

from origin.database.entities.actions import Create
from origin.database.schemas.templates.tasks_templates import TasksTemplates
from origin.envars.origin_envars import ContextHandler


class CreateAssetUI(QtWidgets.QDialog):

    def __init__(self, context, asset_parent=None, parent=None):
        super(CreateAssetUI, self).__init__(parent)

        self.setWindowTitle("Create Asset")
        self.setMinimumWidth(250)
        self.setMinimumHeight(150)

        self.user_data = None
        self.context_handler: ContextHandler = context

        self.asset_parent = asset_parent

        self.show_name_le = QtWidgets.QLabel()

        if self.asset_parent is not None:
            self.show_name_le.setText(self.asset_parent)
        else:
            self.show_name_le.setText(self.context_handler.show_name)

        self.asset_name_le = QtWidgets.QLineEdit()
        self.task_template_cb = QtWidgets.QComboBox()

        self.basic_tasks = QtWidgets.QRadioButton("basic_tasks")
        self.basic_tasks.setChecked(True)
        self.basic_tasks.setDisabled(True)

        self.has_groom_ckb = QtWidgets.QRadioButton("has_groom")
        self.has_groom_cfx_ckb = QtWidgets.QRadioButton("has_groom_cfx")
        self.has_cloth_cfx_ckb = QtWidgets.QRadioButton("has_cloth_cfx")
        self.is_assembly_ckb = QtWidgets.QRadioButton("is_assembly")

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Close")

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("Asset Path: ", self.show_name_le)
        self.form_layout.addRow("Asset Name:", self.asset_name_le)

        self.options_layout = QtWidgets.QGridLayout()
        self.options_layout.addWidget(self.basic_tasks, 0, 0)
        self.options_layout.addWidget(self.has_groom_ckb, 1, 0)
        self.options_layout.addWidget(self.has_groom_cfx_ckb, 1, 1)
        self.options_layout.addWidget(self.has_cloth_cfx_ckb, 2, 0)
        self.options_layout.addWidget(self.is_assembly_ckb, 2, 1)

        button_group = QtWidgets.QButtonGroup(self)
        button_group.addButton(self.has_groom_ckb)
        button_group.addButton(self.has_groom_cfx_ckb)
        button_group.addButton(self.has_cloth_cfx_ckb)
        button_group.addButton(self.is_assembly_ckb)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.create_btn)
        self.buttons_layout.addWidget(self.create_and_close_btn)
        self.buttons_layout.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addStretch(-1)
        self.main_layout.addLayout(self.options_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.buttons_layout)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def get_checked_options(self):
        checked_items = []
        for i in range(self.options_layout.count()):
            item = self.options_layout.itemAt(i)
            widget = item.widget()
            if widget.isChecked():
                checked_items.append(widget.text())

        print(checked_items)
        return checked_items

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        asset_name = self.asset_name_le.text()
        get_selected_options = self.get_checked_options()

        created_asset_id = Create(context=self.context_handler).asset(name=asset_name,
                                                                      parent=self.asset_parent
                                                                      )
        self.context_handler.entity_id = created_asset_id

        tasks_template = TasksTemplates(context=self.context_handler)
        tasks_template.build_base_task_schema()

        options_config = {
            "has_groom": tasks_template.build_has_groom,
            "has_groom_cfx": tasks_template.build_has_groom_cfx,
            "has_cloth_cfx": tasks_template.build_has_cloth_cfx,
            "is_assembly": tasks_template.build_is_assembly,
        }

        for sel_option in get_selected_options:
            if sel_option in list(options_config.keys()):
                options_config[sel_option]()
        tasks_template.create_build_tasks()

        Create(context=self.context_handler).asset_breakdown(parent_id=created_asset_id)

        self.asset_name_le.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateAssetUI()
    create_asset.show()
    sys.exit(app.exec_())
