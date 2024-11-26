from abc import ABC, abstractmethod


class CameraExporter(ABC):

    @abstractmethod
    def save_master_file(self):
        pass

    @abstractmethod
    def get_camera_nodes(self):
        pass

    @abstractmethod
    def set_camera_specs(self):
        pass

    @abstractmethod
    def bake_animation(self):
        pass

    @abstractmethod
    def export_camera(self, export_path, file_format="ma"):
        pass

    @abstractmethod
    def export_alembic(self, export_path):
        pass

    @abstractmethod
    def export_usd(self, export_path):
        pass

    @abstractmethod
    def run_export(self, focal_length=None, filmback=None, resolution_gate=None, export_path=None, file_format="ma"):
        pass
