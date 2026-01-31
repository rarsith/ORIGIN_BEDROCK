import copy
import os

from PySide2 import QtWidgets

from origin.database.statuses import DbVersionStatuses
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

from origin.common_utils import json_utils


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

    def entity_properties(self):
        entity_doc = self.context_handler.database_handler().get_asset_document()
        entity_properties = entity_doc.definition
        return entity_properties

    def get_selected_options(self):
        get_comment_text = self.comment_ptx.toPlainText()
        get_publishing_status = self.status_wdg.currentText()
        get_entity_properties = self.entity_properties()

        return {
            "pub_comment": get_comment_text,
            "pub_status": get_publishing_status,
            "entity_properties": get_entity_properties
        }

    def publish(self, options):
        current_dcc = os.getenv("DCC")
        get_pub_options = self.get_selected_options()
        options.update(get_pub_options)

        if current_dcc != "origin_standalone":
            from origin.dcc.common.batch_processing.batch_processing import BatchProcessing
            from origin.dcc.common.utils.save_session import scene_session_operations_class

            current_scene = scene_session_operations_class()
            master_scene_path = current_scene.save_current_file()
            options["master_scene"] = master_scene_path

            # side save for Doci to pick up - slow transition of the batch processes
            doci_pub_options = copy.deepcopy(options)
            serialized_context = self.context_handler.snapshot_session()
            doci_pub_options['context_object'] = serialized_context
            json_doci = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\origin\applications\Doci\jobs\incoming"
            json_file = "incoming.json"
            json_utils.save_json(target_path=json_doci, target_file=json_file, data=doci_pub_options)


            # continue with existing options --> to be deprecated
            publisher_type = BatchProcessing(options=options, task="publish")
            publisher_type.run()

        else:
            print (f"{current_dcc.upper()} detected. Skipping Batch Processing.")




if __name__ == "__main__":
    pass
    # from origin.ui.tests.manual_cotext import test_ui
    # test_ui(main_widget=Publish)
