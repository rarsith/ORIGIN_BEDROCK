from origin.dcc.extensions.maya.publish.exporters.alembic.alembic import MayaAlembicExporter
from origin.dcc.extensions.maya.publish.exporters.obj.obj import MayaOBJExporter
from origin.dcc.extensions.maya.publish.exporters.scene.master_scene import MayaMasterSceneExporter
from origin.dcc.extensions.maya.publish.exporters.usd.usd import MayaUSDExporter
from origin.envars.origin_envars import ContextHandler

import maya.cmds as cmds


class MayaGeometryExporter:
    obj_file = "obj"
    alembic_file = "abc"
    usd_file = "usd"
    origin_scene_file = "master"
    version_string = "version_string"

    def __init__(self, options, src_file_path=None):
        self.options = options
        self.context_handler = self.options["context_object"]

        if isinstance(self.context_handler, dict):
            self.context_handler = ContextHandler()
            self.context_handler.load_session(self.options["context_object"])

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
            cmds.file(self.src_file_path,
                      i=True,
                      typ="mayaBinary",
                      ignoreVersion=True,
                      ra=True,
                      mergeNamespacesOnClash=False,
                      namespace=":",
                      pr=True,
                      importTimeRange="combine",
                      )

    def export_master_scene(self):
        self.master_file_exporter = MayaMasterSceneExporter(options=self.options,
                                                            context=self.context_handler,
                                                            object_transform="main")

        exported_results = self.master_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_alembic(self):
        self.alembic_file_exporter = MayaAlembicExporter(options=self.options,
                                                         context=self.context_handler,
                                                         object_transform="main|geo")

        exported_results = self.alembic_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_obj(self):
        self.obj_file_exporter = MayaOBJExporter(options=self.options,
                                                 context=self.context_handler,
                                                 object_transform="main|geo")

        exported_results = self.obj_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_usd(self):
        self.usd_file_exporter = MayaUSDExporter(options=self.options,
                                                 context=self.context_handler,
                                                 object_transform="main|geo")

        exported_results = self.usd_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export(self, files_formats: list = None):
        self.open_master_file()
        self.export_master_scene()

        files = {self.alembic_file: self.export_alembic,
                 self.obj_file: self.export_obj,
                 self.usd_file: self.export_usd
                 }

        if files_formats is None:
            files_formats = self.options["user_file_formats"]

        if files_formats is not None:
            for file_type in files_formats:
                if file_type in files:
                    files[file_type]()
        return self.exported_results

