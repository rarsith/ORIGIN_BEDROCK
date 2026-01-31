from origin.dcc.extensions.maya.publish.tasks.abc.batch_task import BatchTask
from origin.dcc.extensions.maya.publish.exporters.geometry import MayaGeometryExporter


class MayaGeometryExporterTask(BatchTask):
    def execute(self):
        src_file_path = self.options.get("master_scene", "")

        obj = MayaGeometryExporter(options=self.options,
                                   src_file_path=src_file_path)

        results = obj.export()
        return results
