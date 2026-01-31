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
    def export_alembic(self):
        pass

    @abstractmethod
    def export_usd(self):
        pass

    @abstractmethod
    def export_camera(self, file_format):
        pass

    @abstractmethod
    def run_export(self, file_format, focal_length=None, filmback=None, resolution_gate=None, cam_motion_blur=False):
        pass


