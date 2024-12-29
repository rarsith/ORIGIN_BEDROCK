import os

from PySide2 import QtWidgets

from origin.common_utils import dict_utils
from origin.dcc.task_type_publisher import PublisherType
from origin.database.statuses import DbVersionStatuses
from origin.envars.origin_envars import ContextHandler
from origin.database.entities.actions import Create


class Publish(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, parent=None):
        super(Publish, self).__init__(parent)

        self.context_handler = context

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

    def populate_existing_comments(self):
        pass

    def get_selected_options(self):
        get_comment_text = self.comment_ptx.toPlainText()
        get_publishing_status = self.status_wdg.currentText()
        return {"pub_comment": get_comment_text, "pub_status": get_publishing_status}

    def create_task_db_asset(self, selected_options):
        create_entity = Create(context=self.context_handler)
        db_asset_id = create_entity.db_asset(parent=self.context_handler.db_asset_stream_id,
                                             publish_type=selected_options["publish_type"])
        return db_asset_id

    def create_db_asset_version(self, selected_options):
        create_entity = Create(context=self.context_handler)
        db_asset_version_id = create_entity.db_asset_version(parent_id=self.context_handler.db_asset_id,
                                                             status=selected_options["pub_status"],
                                                             comment=selected_options["pub_comment"])
        return db_asset_version_id

    def create_db_file_components(self, db_asset_version_id, published_data):
        create_entity = Create(context=self.context_handler)
        for saved_files_categories in published_data:
            if published_data[saved_files_categories] != {}:
                for file_format, file_path in published_data[saved_files_categories].items():
                    origin_root = os.getenv("ORIGIN_PROJECTS_ROOT")
                    relative_path = os.path.relpath(file_path, start=origin_root)
                    create_entity.db_asset_file_component(visibility=True,
                                                          file_ext=file_format,
                                                          file_path=str(relative_path),
                                                          parent_id=db_asset_version_id)

    def create_asset_breakdown_version(self, options):
        curr_breakdown_ver_doc = self.context_handler.database_handler().get_asset_breakdown_latest_version()

        asset_stream_id = self.context_handler.db_asset_stream_id
        asset_stream = asset_stream_id.replace(".", "__") if "." in asset_stream_id else asset_stream_id
        stream_name = asset_stream.rsplit("__", 1)[1]

        asset_breakdown = {asset_stream: {"db_assets": {options["publish_type"]: self.context_handler.db_asset_id}}}

        needs_update = False
        if curr_breakdown_ver_doc is not None:
            current_breakdown = curr_breakdown_ver_doc.data
            if current_breakdown is not None:
                needs_update = dict_utils.is_subset_dict(asset_breakdown, curr_breakdown_ver_doc.data)
                if needs_update:
                    merged_config = dict_utils.merge_dicts(asset_breakdown, curr_breakdown_ver_doc.data)
                    new_db_breakdown_version_id = Create(context=self.context_handler).asset_breakdown_version(data=merged_config)
                    self.context_handler.asset_breakdown_version_id = new_db_breakdown_version_id

                else:
                    self.context_handler.asset_breakdown_version_id = curr_breakdown_ver_doc.id

        else:
            db_breakdown_version_id = Create(context=self.context_handler).asset_breakdown_version(data=asset_breakdown)
            self.context_handler.asset_breakdown_version_id = db_breakdown_version_id

    def create_stack_version(self, options=None):
        Create(context=self.context_handler).asset_stack_version(status="PENDING REVIEW")

    def publish(self, options):
        get_pub_options = self.get_selected_options()
        options.update(get_pub_options)
        db_asset_id = self.create_task_db_asset(selected_options=options)
        self.context_handler.db_asset_id = db_asset_id

        # task_publisher = TaskTypePublisher(publish_options=options)
        task_publisher = PublisherType(publish_options=options)
        published_data = task_publisher.execute_publish()

        db_asset_version_id = self.create_db_asset_version(selected_options=options)
        self.create_db_file_components(db_asset_version_id=db_asset_version_id,
                                       published_data=published_data)

        self.create_asset_breakdown_version(options)
        self.create_stack_version()


if __name__ == "__main__":
    import sys

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

    # context_class = ContextHandler()
    # context_class.load_session(session_data=context_sample)
    #
    # publishing_options = {'db_asset_id': 'New_State.assets.chr.yellow_hulk.modeling.gloves_metalic',
    #                       'db_asset_qc': 'OK',
    #                       'file_formats': ['ABC', 'USD', 'OBJ'],
    #                       'all_sets_assigned': [],
    #                       'inject_textures_path': None,
    #                       'bundle_stream_id': '',
    #                       'review_options': ['Playblast'],
    #                       'pub_comment': 'asdfasdfzdf',
    #                       'pub_status': 'IN PROGRESS',
    #                       'context_object': context_class}

    DATA = {'data':
        {
            'master': 'X:/projects/The_Rock/assets/chr/tafer/modeling/publishes/data/geometry__tafer__tafarMain/chr__tafer__tafarMain__v0003/origin_scene/chr__tafer__tafarMain__v0003.mb',
            'abc': 'X:/projects/The_Rock/assets/chr/tafer/modeling/publishes/data/geometry__tafer__tafarMain/chr__tafer__tafarMain__v0003/alembic/chr__tafer__tafarMain__v0003.abc',
            'usd': 'X:/projects/The_Rock/assets/chr/tafer/modeling/publishes/data/geometry__tafer__tafarMain/chr__tafer__tafarMain__v0003/USD/chr__tafer__tafarMain__v0003.usd',
            'obj': 'X:/projects/The_Rock/assets/chr/tafer/modeling/publishes/data/geometry__tafer__tafarMain/chr__tafer__tafarMain__v0003/obj/chr__tafer__tafarMain__v0003.obj'},
        'images': {},
        'quicktime': {}
    }

    print(DATA.keys())

    # app = QtWidgets.QApplication(sys.argv)
    # test_dialog = Publish(context=context_class)
    # test_dialog.publish(options=DATA)
    #
    # test_dialog.show()
    # sys.exit(app.exec_())
