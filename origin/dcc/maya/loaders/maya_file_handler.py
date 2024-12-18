import os
import maya.cmds as cmds
import maya.mel as mel


class MayaFileHandler:
    """
    A utility class to open or reference files in Maya based on a file path.
    """

    SUPPORTED_EXTENSIONS = {".ma", ".mb", ".abc", ".obj", ".usd"}

    def __init__(self, file_path):
        """
        Initialize the handler with a file path.
        :param file_path: Path to the file to open or reference.
        """
        self.file_path = self.convert_to_valid_path(file_path)
        self.extension = os.path.splitext(file_path)[1].lower()

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")

        if self.extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file extension: {self.extension}")

    def get_file_types_ops(self):
        file_types_ops = {".ma": ["reference", "open", "import"],

                          ".mb": ["reference", "open", "import"],

                          ".obj": ["reference", "import"],

                          ".abc": ["reference", "import"],

                          ".usd": ["import"]
                          }

        return self.extension, file_types_ops.get(self.extension)

    def execute_file_ops(self, operation):
        file_types_ops = {".ma": {"reference": self.reference_file,
                                  "open": self.open_file,
                                  "import": self.import_file},

                          ".mb": {"reference": self.reference_file,
                                  "open": self.open_file,
                                  "import": self.import_file},

                          ".obj": {"reference": self.reference_file,
                                   "import": self.import_file},

                          ".abc": {"reference": self.reference_file,
                                   "import": self.import_file},

                          ".usd": {"reference": self.import_file,
                                   "import": self.import_file}
                          }

        file_op = file_types_ops[self.extension][operation]
        return file_op()

    def open_file(self):
        """
        Open the file in Maya, replacing the current scene.
        """
        if self.extension in {".ma", ".mb"}:
            cmds.file(f=True, new=True)
            cmds.file(self.file_path,
                      open=True,
                      force=True,
                      loadReferenceDepth="none",
                      ignoreVersion=True,
                      preserveReferences=True)

        elif self.extension == ".usd":
            cmds.file(self.file_path,
                      open=True,
                      type="USD Import",
                      loadReferenceDepth="none",
                      force=True,
                      ignoreVersion=True,
                      preserveReferences=True)
        else:
            raise ValueError(f"Opening not supported for: {self.extension}")

    def reference_file(self, namespace=None):
        """
        Reference the file into the current Maya session.
        :param namespace: Optional namespace for the reference.
        """
        namespace = namespace or os.path.splitext(os.path.basename(self.file_path))[0]

        if self.extension in {".ma", ".mb"}:
            cmds.file(self.file_path, reference=True, namespace=namespace)
        elif self.extension == ".abc":
            cmds.file(self.file_path, reference=True, namespace=namespace)
        elif self.extension == ".usd":
            cmds.file(self.file_path, reference=True, type="USD Import", namespace=namespace)
        elif self.extension == ".fbx":
            mel.eval(f"FBXImport -f \"{self.file_path}\";")
        elif self.extension == ".obj":
            cmds.file(self.file_path, i=True, type="OBJ")
        else:
            raise ValueError(f"Referencing not supported for: {self.extension}")

    def import_file(self, namespace=None):
        namespace = namespace or os.path.splitext(os.path.basename(self.file_path))[0]

        if self.extension in {".ma", ".mb"}:
            cmds.file(self.file_path, i=True, namespace=namespace)
        elif self.extension == ".abc":
            cmds.file(self.file_path, i=True, namespace=namespace)
        elif self.extension == ".usd":
            cmds.file(self.file_path, i=True, type="USD Import", namespace=namespace)
        elif self.extension == ".obj":
            cmds.file(self.file_path, i=True, type="OBJ", namespace=namespace)
        else:
            raise ValueError(f"Importing not supported for: {self.extension}")

    def convert_to_valid_path(self, raw_path):
        """
        Convert a raw path into a valid path for the operating system.
        :param raw_path: Raw file path to convert.
        :return: Validated and converted file path.
        """
        # Replace forward slashes with the correct OS separator
        normalized_path = os.path.normpath(raw_path)

        # Check if the path exists
        if not os.path.exists(normalized_path):
            raise FileNotFoundError(f"The path does not exist: {normalized_path}")

        return normalized_path


if __name__ == "__main__":
    file_path = r"X:\projects\The_Rock\assets\chr\tafer\modeling\publishes\data\geometry__tafer__tafer_main\chr__tafer__tafer_main__v0006\alembic\chr__tafer__tafer_main__v0006.abc"
    main_proc = MayaFileHandler(file_path=file_path)
    file_op_type = main_proc.execute_file_ops("reference")
    print(file_op_type)
