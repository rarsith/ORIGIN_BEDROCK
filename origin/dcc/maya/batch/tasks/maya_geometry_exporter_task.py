from origin.dcc.maya.batch.tasks.abc.batch_task import BatchTask
from origin.dcc.maya.exporters.XXgeometry import MayaGeometryExporter
from origin.dcc.maya.exporters.maya_make_playblast import MayaMakePlayblast


class MayaGeometryExporterTask(BatchTask):
    def execute(self):
        src_file_path = self.options.get("master_scene", "")

        obj = MayaGeometryExporter(options=self.options,
                                   src_file_path=src_file_path)

        obj.export()
