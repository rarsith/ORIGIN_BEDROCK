from origin.envars.origin_envars import ContextHandler


class MariPublisher:
    def __init__(self, publish_options):
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]


    def publish(self):
        print(f"Publishing with options {self.publishing_options}")
