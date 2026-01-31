from origin.dcc.publishers.handler import publish_type_switcher


class PublisherType:
    def __init__(self, publish_options):
        self.publishing_options = publish_options

        self.publisher_type = publish_type_switcher.get_publish_type_class(publish_options["publish_type"])

    def execute_publish(self):
        publish_results = self.publisher_type(options=self.publishing_options).publish()
        return publish_results
