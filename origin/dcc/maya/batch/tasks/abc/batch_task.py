from abc import ABC, abstractmethod


class BatchTask(ABC):
    def __init__(self, options):
        self.options = options

    @abstractmethod
    def execute(self):
        pass
