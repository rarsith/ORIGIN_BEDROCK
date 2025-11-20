from PySide2 import QtWidgets

from origin.dcc.maya.batch.maya_batch import BatchProcessing
from origin.dcc.save_session import scene_session_operations_class
from origin.database.statuses import DbVersionStatuses
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


class Publish(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, parent=None):
        super(Publish, self).__init__(parent)

        self.context_handler = context
        self.path_handler = OriginOSPathHandler(context=self.context_handler)
        self.db_publisher = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.comment_ptx = QtWidgets.QPlainTextEdit()
        self.pub_status_lb = QtWidgets.QLabel("Publish with Status:")
        self.status_wdg = QtWidgets.QComboBox()
        self.status_wdg.addItems(DbVersionStatuses().list_publish_statuses())
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

    def populate_existing_comments(self):
        pass

    def get_selected_options(self):
        get_comment_text = self.comment_ptx.toPlainText()
        get_publishing_status = self.status_wdg.currentText()
        return {"pub_comment": get_comment_text, "pub_status": get_publishing_status}

    def publish(self, options):
        get_pub_options = self.get_selected_options()
        options.update(get_pub_options)

        current_scene = scene_session_operations_class()
        master_scene_path = current_scene.save_current_file()
        options["master_scene"] = master_scene_path

        publisher_type = BatchProcessing(options=options, task="publish")
        publisher_type.run()


if __name__ == "__main__":
   pass
