import inspect
from PySide2 import QtWidgets

from origin.envars.origin_envars import ContextHandler
from origin.database.entities.operators import PublishOptions
from origin.ui.publish.playblast_options.playblast_options_ui import PlayblastOptionsUI
from origin.ui.publish.utils.publishing_type_widgets_factory import get_publish_type


class OriginPublisher(QtWidgets.QDialog):
    def __init__(self, context: ContextHandler, publish_type=None, parent=None):
        super(OriginPublisher, self).__init__(parent)

        self.setWindowTitle("Publish")

        self.setMinimumWidth(500)
        self.setMinimumHeight(420)

        self.context_handler = context
        self.publish_type = publish_type

        self.publish_options = PublishOptions()

        context_task_type = get_publish_type(context=context, pub_type=self.publish_type)
        self.widgets = context_task_type

        self.current_step = 0

        self.collected_options = {"publish_type": self.publish_type}

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.load_widgets()

        self.playblast_widget = PlayblastOptionsUI(context=self.context_handler)
        self.playblast_widget.playblast_btn.setEnabled(False)
        self.playblast_widget.playblast_btn.setVisible(False)
        self.playblast_widget.cancel_bn.setEnabled(False)
        self.playblast_widget.cancel_bn.setVisible(False)

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

    def resolve_preview_widgets(self):
        if "review_medium" in list(self.collected_options.keys()) and self.collected_options["review_medium"] == "playblast":
            if self.playblast_widget not in self.widgets:
                self.widgets.insert(self.current_step, self.playblast_widget)
        else:
            if self.playblast_widget in self.widgets:
                get_index = self.widgets.index(self.playblast_widget)
                self.widgets.remove(self.playblast_widget)

    def clear_stacked_widget(self, stacked_widget):
        while stacked_widget.count() > 0:
            widget = stacked_widget.widget(0)
            stacked_widget.removeWidget(widget)

    def load_widgets(self):
        self.clear_stacked_widget(self.widget_container)

        for widget in self.widgets:
            if hasattr(widget, "reinitialize"):
                widget.reinitialize(pub_options=self.collected_options)
            self.widget_container.addWidget(widget)
        self.widget_container.setCurrentIndex(0)

    def load_next_widget(self):
        self.back_btn.setDisabled(False)

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
            self.resolve_preview_widgets()
            self.load_widgets()

            self.widget_container.setCurrentIndex(self.current_step)

            if self.current_step == len(self.widgets) - 1:
                self.next_btn.setText("Publish")
                self.current_step = len(self.widgets) - 1
            else:
                self.next_btn.setText("Next")

        else:
            self.start_publishing()

    def load_previous_widget(self):
        current_widget = self.widgets[self.current_step]
        first_widget = self.widgets[0]

        if not self.current_step <= 0:
            current_widget = self.widgets[self.current_step]

        self.current_step -= 1
        self.widget_container.setCurrentIndex(self.current_step)

        if current_widget != first_widget and self.current_step < len(self.widgets):
            current_active_widget = self.widgets[self.current_step]
            get_current_widget_options = current_active_widget.get_selected_options()

            for option in get_current_widget_options:
                del self.collected_options[option]

        self.resolve_preview_widgets()

        if self.current_step == len(self.widgets) - 1:
            self.next_btn.setText("Publish")
            self.current_step = len(self.widgets) - 1
        else:
            self.next_btn.setText("Next")

        if self.current_step == 0:
            self.back_btn.setDisabled(True)
        else:
            self.back_btn.setDisabled(False)

    def save_widget_options(self, widget):
        widget_selected_options = widget.get_selected_options()
        if widget_selected_options is not None:
            self.collected_options.update(widget.get_selected_options())
            print(self.collected_options)
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
