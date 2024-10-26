from origin.envars.Xorigin_envars import ContextHandler

class MayaPublisher:
    def __init__(self, publish_options):
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]

    def publish(self):
        print(f"Publishing using {self.publish_type} and with options {self.publishing_options}")
