import sys
from PySide2 import QtWidgets

from origin.envars.Xorigin_envars import ContextHandler
from o_database.entities.Xactions import Create


class CreateGroupUI(QtWidgets.QDialog):

    def __init__(self, context, group_parent=None, parent=None):
        super(CreateGroupUI, self).__init__(parent)

        self.setWindowTitle("Create Group")

        self.user_data = None

        self.context_handler = ContextHandler()
        self.context_handler.load_session(context)

        self.group_parent = group_parent

        self.show_name_le = QtWidgets.QLabel()

        if self.group_parent is not None:
            self.show_name_le.setText(self.group_parent)
        else:
            self.show_name_le.setText(self.context_handler.show_name)

        self.group_name_le = QtWidgets.QLineEdit()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("Group Path: ", self.show_name_le)
        self.form_layout.addRow("Group Name:", self.group_name_le)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.create_btn)
        self.buttons_layout.addWidget(self.create_and_close_btn)
        self.buttons_layout.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.buttons_layout)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)


    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        asset_name = self.group_name_le.text()
        context = self.context_handler.snapshot_session()

        Create(context=context).group(name=asset_name,
                                      parent=self.group_parent
                                      )
        self.group_name_le.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateGroupUI()
    create_asset.show()
    sys.exit(app.exec_())