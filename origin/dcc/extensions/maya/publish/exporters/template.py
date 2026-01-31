from origin.dcc.extensions.maya.publish.exporters.scene.master_scene import MayaMasterSceneExporter
from origin.dcc.extensions.maya.publish.exporters.usd.usd import MayaUSDExporter
from origin.envars.origin_envars import ContextHandler

import maya.cmds as cmds


class MayaPlayblastTemplateExporter:
    usd_file = "usd"
    origin_scene_file = "master"
    maya_scene = "maya_scene"
    version_string = "version_string"

    def __init__(self, options, src_file_path=None):
        self.options = options
        self.context_handler = self.options["context_object"]

        if isinstance(self.context_handler, dict):
            self.context_handler = ContextHandler()
            self.context_handler.load_session(self.options["context_object"])

        print("--------------TEMPLATE EXPORT RESOLVED CONTEXT: ", self.context_handler.snapshot_session())

        self.src_file_path = src_file_path

        if self.src_file_path is None:
            self.src_file_path = self.options["master_scene"]

        self.master_file_exporter = None
        self.alembic_file_exporter = None
        self.obj_file_exporter = None
        self.usd_file_exporter = None

        self.exported_results = {}

    def open_master_file(self):
        if self.src_file_path is not None:
            cmds.file(self.src_file_path, open=True, force=True)

    def export_master_scene(self):
        self.master_file_exporter = MayaMasterSceneExporter(options=self.options,
                                                            context=self.context_handler)

        exported_results = self.master_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_usd(self):
        self.usd_file_exporter = MayaUSDExporter(options=self.options,
                                                 context=self.context_handler,
                                                 object_transform="main|template")

        exported_results = self.usd_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export(self, files_formats: list = None):
        self.open_master_file()
        # self.export_master_scene()
        files = {self.origin_scene_file: self.export_master_scene,
                 self.usd_file: self.export_usd
                 }

        files_formats = [self.origin_scene_file, self.usd_file]

        if files_formats is not None:
            for file_type in files_formats:
                if file_type in files.keys():
                    files[file_type]()
        return self.exported_results
