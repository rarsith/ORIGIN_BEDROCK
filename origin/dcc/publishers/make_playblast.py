import os
from origin.dcc.maya.exporters.maya_make_playblast import MayaMakePlayblast
from origin.envars.origin_envars import ContextHandler


class MakePlayblast:
    def __init__(self, options=None):
        self.exported_results = {"frames": []}
        self.publishing_options = options
        if self.publishing_options is not None:
            self.context_handler: ContextHandler = self.publishing_options["context_object"]

        self.dcc = os.getenv("DCC")
        self.make_playblast_class = self.get_playblast_class(dcc=self.dcc)

    def get_playblast_class(self, dcc):
        classes = {
            "maya": MayaMakePlayblast(options=self.publishing_options)
            # "blender": BlenderBatchScript(context=self.context_handler),
        }
        if dcc in list(classes.keys()):
            return classes[dcc]

    def execute(self):
        self.make_playblast_class = self.get_playblast_class(dcc=self.dcc)
        self.make_playblast_class.execute()

        return self.exported_results


if __name__ == "__main__":
    pass
