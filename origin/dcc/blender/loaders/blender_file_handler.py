import os
import bpy

class BlenderFileHandler:
    """
    A utility class to open or link files in Blender based on a file path.
    """

    SUPPORTED_EXTENSIONS = {".blend", ".abc", ".fbx", ".obj", ".usd"}

    def __init__(self, file_path):
        """
        Initialize the handler with a file path.
        :param file_path: Path to the file to open or link.
        """
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")

        if self.extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {self.extension}")

    def open_file(self):
        """
        Open the file in Blender, replacing the current scene.
        """
        if self.extension == ".blend":
            bpy.ops.wm.open_mainfile(filepath=self.file_path)
        else:
            raise ValueError(f"Opening not supported for: {self.extension}")

    def link_file(self, group_name=None):
        """
        Link the file into the current Blender session.
        :param group_name: Optional group name for linked data.
        """
        if self.extension == ".blend":
            with bpy.data.libraries.load(self.file_path, link=True) as (data_from, data_to):
                data_to.collections = data_from.collections
            if group_name:
                for collection in data_to.collections:
                    collection.name = group_name
        elif self.extension == ".abc":
            bpy.ops.wm.alembic_import(filepath=self.file_path)
        elif self.extension == ".fbx":
            bpy.ops.import_scene.fbx(filepath=self.file_path)
        elif self.extension == ".obj":
            bpy.ops.import_scene.obj(filepath=self.file_path)
        elif self.extension == ".usd":
            bpy.ops.wm.usd_import(filepath=self.file_path)
        else:
            raise ValueError(f"Linking not supported for: {self.extension}")

# Example usage:
# file_handler = BlenderFileHandler("/path/to/your/file.blend")
# file_handler.open_file()
# file_handler.link_file(group_name="MyGroup")
