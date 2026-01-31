from origin.dcc.common.abc.geometry_exporter import GeometryExporter
from origin.envars.origin_envars import ContextHandler


class BlenderGeometryExporter(GeometryExporter):
    obj_file = "obj"
    alembic_file = "abc"
    usd_file = "usd"
    origin_scene_file = "master"
    version_string = "version_string"

    def __init__(self, objects_names: list, context: ContextHandler):
        self.objects_names = objects_names
        self.context_handler = context
        self.path_handler = None


    def save_master_file(self):
        pass

    def export_alembic(self,
                       frame_range=(1, 1),
                       uv_write=True,
                       world_space=True,
                       write_uv_sets=True,
                       data_format="ogawa"):
        pass

    def export_obj(self):
        pass

    def export_usd(self):
        pass

    def export_geometry(self, file_format):
        pass
