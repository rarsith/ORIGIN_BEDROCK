import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QLabel, \
    QLineEdit


class Menu1(QWidget):
    def __init__(self, parent=None):
        super(Menu1, self).__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Select asset to publish:")
        self.input_field = QLineEdit()
        self.next_button = QPushButton("Next")
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.next_button)
        self.setLayout(layout)


class Menu2(QWidget):
    def __init__(self, parent=None):
        super(Menu2, self).__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Specify version and description:")
        self.version_label = QLabel("Version:")
        self.version_input = QLineEdit()
        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit()
        self.next_button = QPushButton("Next")
        layout.addWidget(self.label)
        layout.addWidget(self.version_label)
        layout.addWidget(self.version_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.next_button)
        self.setLayout(layout)


class Menu3(QWidget):
    def __init__(self, parent=None):
        super(Menu3, self).__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Choose destination path:")
        self.destination_label = QLabel("Destination Path:")
        self.destination_input = QLineEdit()
        self.next_button = QPushButton("Next")
        layout.addWidget(self.label)
        layout.addWidget(self.destination_label)
        layout.addWidget(self.destination_input)
        layout.addWidget(self.next_button)
        self.setLayout(layout)


class Menu4(QWidget):
    def __init__(self, parent=None):
        super(Menu4, self).__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Review publishing details:")
        self.summary_label = QLabel()
        self.finish_button = QPushButton("Finish")
        layout.addWidget(self.label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.finish_button)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.menu1 = Menu1()
        self.menu2 = Menu2()
        self.menu3 = Menu3()
        self.menu4 = Menu4()

        self.stacked_widget.addWidget(self.menu1)
        self.stacked_widget.addWidget(self.menu2)
        self.stacked_widget.addWidget(self.menu3)
        self.stacked_widget.addWidget(self.menu4)

        self.menu1.next_button.clicked.connect(self.show_menu2)
        self.menu2.next_button.clicked.connect(self.show_menu3)
        self.menu3.next_button.clicked.connect(self.show_menu4)
        self.menu4.finish_button.clicked.connect(self.publish_asset)

        self.publishing_data = {}

    def show_menu2(self):
        self.publishing_data['asset_file'] = self.menu1.input_field.text()
        self.stacked_widget.setCurrentWidget(self.menu2)

    def show_menu3(self):
        self.publishing_data['version'] = self.menu2.version_input.text()
        self.publishing_data['description'] = self.menu2.description_input.text()
        self.stacked_widget.setCurrentWidget(self.menu3)

    def show_menu4(self):
        self.publishing_data['destination_path'] = self.menu3.destination_input.text()
        summary = f"Asset File: {self.publishing_data['asset_file']}\nVersion: {self.publishing_data['version']}\nDescription: {self.publishing_data['description']}\nDestination Path: {self.publishing_data['destination_path']}"
        self.menu4.summary_label.setText(summary)
        self.stacked_widget.setCurrentWidget(self.menu4)

    def publish_asset(self):
        # Generate final publishing string
        final_publishing_string = f"Publishing Asset:\n"
        final_publishing_string += f"Asset File: {self.publishing_data['asset_file']}\n"
        final_publishing_string += f"Version: {self.publishing_data['version']}\n"
        final_publishing_string += f"Description: {self.publishing_data['description']}\n"
        final_publishing_string += f"Destination Path: {self.publishing_data['destination_path']}\n"
        print(final_publishing_string)
        # Here you would implement the actual publishing logic, such as copying the file to the specified destination
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 400, 200)
    window.show()
    sys.exit(app.exec_())
