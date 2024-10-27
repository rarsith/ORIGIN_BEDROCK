from PySide2 import QtWidgets

from origin.envars.origin_envars import ContextHandler
from origin.database.entities.operators import PublishOptions
from origin.ui.publish.utils.publishing_widgets_factory import get_publish_type


class OriginPublisher(QtWidgets.QDialog):
    def __init__(self, context, parent=None):
        super(OriginPublisher, self).__init__(parent)

        self.setWindowTitle("Publish")

        self.setMinimumWidth(400)
        self.setMinimumHeight(200)

        self.context_handler = context

        self.publish_options = PublishOptions()

        context_task_type = get_publish_type(context=context)
        self.widgets = context_task_type

        self.current_step = 0

        self.collected_options = {}

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.load_widgets()

    def create_widgets(self):
        self.next_btn = QtWidgets.QPushButton("Next")
        self.back_btn = QtWidgets.QPushButton("Back")

    def create_layout(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.back_btn)
        buttons_layout.addWidget(self.next_btn)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.widget_container = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.widget_container)
        self.main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.next_btn.clicked.connect(self.load_next_widget)
        self.back_btn.clicked.connect(self.load_previous_widget)

    def load_widgets(self):
        for widget in self.widgets:
            self.widget_container.addWidget(widget)

        self.widget_container.setCurrentIndex(0)

    def load_next_widget(self):
        current_widget = self.widgets[self.current_step]
        final_widget = self.widgets[-1]

        options_status = ""
        if current_widget != final_widget:
            options_status = self.save_widget_options(current_widget)

        if options_status is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please perform actions in the interface")
            return

        self.current_step += 1
        if self.current_step < len(self.widgets):
            self.widget_container.setCurrentIndex(self.current_step)

            if self.current_step == len(self.widgets) - 1:
                self.next_btn.setText("Publish")
                self.current_step = len(self.widgets) - 1
            else:
                self.next_btn.setText("Next")
        else:
            self.start_publishing()

    def load_previous_widget(self):
        if self.current_step == 0:
            self.back_btn.setDisabled(True)
            return

        current_widget = ""

        if not self.current_step < 0:
            current_widget = self.widgets[self.current_step]

        self.current_step -= 1

        final_widget = self.widgets[-1]

        if current_widget != final_widget:
            self.save_widget_options(current_widget)

        if self.current_step < len(self.widgets):
            self.widget_container.setCurrentIndex(self.current_step)

            if self.current_step == 0:
                self.back_btn.setDisabled(True)
            else:
                self.back_btn.setDisabled(False)

    def save_widget_options(self, widget):
        widget_selected_options = widget.get_selected_options()
        if widget_selected_options is not None:
            self.collected_options.update(widget.get_selected_options())
            return widget_selected_options
        else:
            return widget_selected_options

    def start_publishing(self):
        final_widget = self.widgets[-1]
        final_widget.publish(self.collected_options)
        self.close()
        QtWidgets.QMessageBox.information(self, "Publishing",
                                          "Publishing process started with options: " + str(self.collected_options))


if __name__ == "__main__":
    import sys
    import os

    os.environ["DCC"] = "nuke"

    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'yellow_hulk',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.yellow_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      }

    context_class = ContextHandler()
    context_class.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = OriginPublisher(context=context_class)

    test_dialog.show()
    sys.exit(app.exec_())
