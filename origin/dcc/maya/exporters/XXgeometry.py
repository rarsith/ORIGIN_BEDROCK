from pathlib import Path
from typing import Literal

from origin.dcc.abc.geometry_exporter import GeometryExporter
from origin.dcc.maya.exporters.alembic.alembic import MayaAlembicExporter
from origin.dcc.maya.exporters.obj.obj import MayaOBJExporter
from origin.dcc.maya.exporters.scene.master_scene import MayaMasterSceneExporter
from origin.dcc.maya.exporters.usd.usd import MayaUSDExporter
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
                      namespace="source_file_sc",
                      pr=True,
                      importTimeRange="combine",
                      )

    def export_alembic(self):
        self.alembic_file_exporter = MayaAlembicExporter(context=self.context_handler,
                                                         object_transform=["source_file_sc:main|source_file_sc:geo"])

        exported_results = self.alembic_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_obj(self):
        self.obj_file_exporter = MayaOBJExporter(context=self.context_handler,
                                                 object_transform=["source_file_sc:main|source_file_sc:geo"])

        exported_results = self.obj_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_usd(self):
        self.usd_file_exporter = MayaUSDExporter(context=self.context_handler,
                                                 object_transform=["source_file_sc:main|source_file_sc:geo"])

        exported_results = self.usd_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export(self, files_formats: list = None):
        self.open_master_file()
        # self.origin_scene_file: self.export_master_file,
        files = {
                 self.alembic_file: self.export_alembic,
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

