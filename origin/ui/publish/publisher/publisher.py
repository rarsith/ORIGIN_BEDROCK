import copy
import os
import shutil
import subprocess
import sys
import time

from PySide2 import QtWidgets

from origin.database.publisher.db_publisher import DBPublisher
from origin.database.statuses import DbVersionStatuses
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

from origin.common_utils import json_utils

def wait_for_file(path, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(path):
            try:
                with open(path, "r"):
                    return True
            except IOError:
                pass
        time.sleep(1.0)
    return False


class Publish(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, parent=None):
        super(Publish, self).__init__(parent)

        self.context_handler = context
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

    def set_db_asset_id(self, pub_options):
        db_publisher = DBPublisher(options=pub_options)
        db_asset_id = db_publisher.create_db_asset(context=self.context_handler,
                                                   parent=self.context_handler.db_asset_stream_id,
                                                   publish_type=pub_options['publish_type'])

        self.context_handler.db_asset_id = db_asset_id

    def publish(self, options):
        current_dcc = os.getenv("DCC")
        app_bin = os.getenv("APP_BIN")
        get_pub_options = self.get_selected_options()
        options.update(get_pub_options)
        options['dcc'] = current_dcc
        options['app_bin'] = app_bin

        self.set_db_asset_id(pub_options=options)

        path_handler = OriginOSPathHandler(context=self.context_handler.snapshot_session(), file_format="json")

        if current_dcc != "origin_standalone":
            from origin.dcc.common.utils.save_session import scene_session_operations_class

            # save current maya wip scene
            current_scene = scene_session_operations_class()
            master_scene_path = current_scene.save_current_file()
            options["master_scene"] = master_scene_path

            # side save for Doci to pick up - slow transition of the batch processes
            doci_pub_options = copy.deepcopy(options)
            serialized_context = self.context_handler.snapshot_session()
            doci_pub_options['context_object'] = serialized_context
            json_doci_temp_path = path_handler.doci_temp_path()
            json_file = path_handler.doci_file_name() + '.json'
            json_doci_path = path_handler.doci_incoming_path()


            # save json publish file for Doci to pick up
            temp_json_file = json_utils.save_json(target_path=json_doci_temp_path, target_file=json_file, data=doci_pub_options)
            shutil.move(temp_json_file, json_doci_path)

        else:
            print (f"{current_dcc.upper()} detected. Skipping Batch Processing.")




if __name__ == "__main__":
    pass
    # from origin.ui.tests.manual_cotext import test_ui
    # test_ui(main_widget=Publish)
