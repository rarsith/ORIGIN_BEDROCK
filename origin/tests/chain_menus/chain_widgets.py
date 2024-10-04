from PySide2 import QtWidgets, QtCore


class PublishingModule(QtWidgets.QWidget):
    def __init__(self, context_type):
        super().__init__()

        self.context_type = context_type
        self.current_step = 0
        self.collected_options = {}  # Store user selections across steps

        # Layout for the dynamic widgets
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.widget_container = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.widget_container)

        # Buttons for navigation
        self.next_button = QtWidgets.QPushButton("Next")
        self.back_button = QtWidgets.QPushButton("Back")
        self.main_layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.load_next_widget)

        # Load widgets based on context
        self.load_widgets()

    def load_widgets(self):
        # Define the widget order based on context
        if self.context_type == "asset":
            self.widgets = [AssetStep1(), AssetStep2(), FinalStep()]
        elif self.context_type == "shot":
            self.widgets = [ShotStep1(), ShotStep2(), FinalStep()]
        else:
            raise ValueError("Unknown context type")

        # Add widgets to the stacked layout
        for widget in self.widgets:
            self.widget_container.addWidget(widget)

        # Show the first widget
        self.widget_container.setCurrentIndex(0)

    def load_next_widget(self):
        # Save current widget's options before moving to the next step
        current_widget = self.widgets[self.current_step]
        final_widget = self.widgets[-1]

        if current_widget != final_widget:
            self.save_widget_options(current_widget)

        self.current_step += 1
        if self.current_step < len(self.widgets):
            self.widget_container.setCurrentIndex(self.current_step)

            # If we are on the last widget, trigger the publishing process
            if self.current_step == len(self.widgets) - 1:
                self.next_button.setText("Publish")
            else:
                self.next_button.setText("Next")
        else:
            self.start_publishing()

    def save_widget_options(self, widget):
        # Collect user input from the current widget (implement this in each widget)
        self.collected_options.update(widget.get_selected_options())

        print(self.collected_options)

    def start_publishing(self):
        # Use the collected options to start the publishing procedure
        final_widget = self.widgets[-1]
        final_widget.publish(self.collected_options)

        QtWidgets.QMessageBox.information(self, "Publishing",
                                          "Publishing process started with options: " + str(self.collected_options))


# Example Widget classes for 'asset' context
class AssetStep1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.option_field = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Asset Step 1: Enter Option"))
        layout.addWidget(self.option_field)

    def get_selected_options(self):
        # Return the selected option as a dictionary
        return {"asset_option_1": self.option_field.text()}


class AssetStep2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.option_field = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Asset Step 2: Enter Option"))
        layout.addWidget(self.option_field)

    def get_selected_options(self):
        return {"asset_option_2": self.option_field.text()}


# Example Widget classes for 'shot' context
class ShotStep1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.option_field = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Shot Step 1: Enter Option"))
        layout.addWidget(self.option_field)

    def get_selected_options(self):
        return {"shot_option_1": self.option_field.text()}


class ShotStep2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.option_field = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Shot Step 2: Enter Option"))
        layout.addWidget(self.option_field)

    def get_selected_options(self):
        return {"shot_option_2": self.option_field.text()}


# Final step widget
class FinalStep(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Final Step: Ready to Publish")
        layout.addWidget(self.label)

    def publish(self, options):
        # Use the collected options to initiate the publishing process
        print("Publishing with options:", options)


# Main Application
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Example usage based on context
    context_type = "asset"  # This can be dynamically set to 'asset' or 'shot'
    window = PublishingModule(context_type)
    window.show()

    app.exec_()
