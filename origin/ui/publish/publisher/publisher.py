from PySide2 import QtWidgets

from o_database.odb_statuses import DbVersionStatuses
from origin.envars.Xorigin_envars import ContextHandler


class Publish(QtWidgets.QWidget):
    def __init__(self, context=None, parent=None):
        super(Publish, self).__init__(parent)

        self.context_handler = ContextHandler()
        self.context_handler.load_session(context)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.comment_ptx = QtWidgets.QPlainTextEdit()
        self.pub_status_lb = QtWidgets.QLabel("Publish with Status:")
        self.status_wdg = QtWidgets.QComboBox()
        self.status_wdg.addItems(DbVersionStatuses().list_all())
        self.previous_comments_ptx = QtWidgets.QPlainTextEdit()

    def create_layout(self):
        pub_status_layout = QtWidgets.QHBoxLayout()
        pub_status_layout.addWidget(self.pub_status_lb)
        pub_status_layout.addWidget(self.status_wdg)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.comment_ptx)
        self.main_layout.addLayout(pub_status_layout)
        self.main_layout.addWidget(self.previous_comments_ptx)

    def create_connections(self):
        pass

    def get_selected_options(self):
        get_comment_text = self.comment_ptx.toPlainText()
        get_publishing_status = self.status_wdg.currentText()
        return {"pub_comment": get_comment_text, "pub_status": get_publishing_status}

    def publish(self, options):
        get_pub_options = self.get_selected_options()
        add_current_options = options.update(get_pub_options)
        print("Publishing with Options: ", add_current_options)

