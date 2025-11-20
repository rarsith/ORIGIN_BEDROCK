import os


class GafferFileHandler:

    SUPPORTED_EXTENSIONS = {".abc", ".usd", ".gfr", ".grf"}

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

