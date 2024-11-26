from abc import ABC, abstractmethod


class GeometryExporter(ABC):

    @abstractmethod
    def save_master_file(self):
        """
        - implementation for saving the current DCC scene from where all the other exports will be derived from

        """
        pass

    @abstractmethod
    def export_alembic(self,
                       frame_range=(1, 1),
                       uv_write=True,
                       world_space=True,
                       write_uv_sets=True,
                       data_format="ogawa"):
        """
        implementation for exporting Alembic file format DCC specific

        Args:
            frame_range: in case of shot export, this could be used to specify the framerange
            uv_write:
            world_space:
            write_uv_sets:
            data_format:

        Returns:

        """

        pass

    @abstractmethod
    def export_obj(self):
        """
        implementation for exporting OBJ file format DCC specific
        Returns:

        """
        pass

    @abstractmethod
    def export_usd(self):
        """
        implementation for exporting USD file format DCC specific
        Returns:

        """
        pass

    @abstractmethod
    def export_geometry(self, file_format):
        """
        Implementation of automatic method to be used based on the inputted options

        Args:
            file_format:

        Returns:

        """
        pass
