from abc import ABC, abstractmethod


class AnimationRigExporter(ABC):

    @abstractmethod
    def save_master_file(self):
        """
        - implementation for saving the current DCC scene from where all the other exports will be derived from

        """
        pass

    @abstractmethod
    def save_maya_scene(self):
        pass

    @abstractmethod
    def export_rigging(self, file_format):
        pass
