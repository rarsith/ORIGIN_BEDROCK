import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QToolButton
from PySide2.QtGui import QIcon

class SoftwareLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Software Launcher')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.software_entries = {}

        # Entry name and path input fields
        self.name_input = QLineEdit()
        self.path_input = QLineEdit()
        self.layout.addWidget(QLabel('Enter DCC name:'))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel('Enter path to executable:'))
        self.layout.addWidget(self.path_input)

        # Add Software button
        add_button = QPushButton('Add Software')
        add_button.clicked.connect(self.add_software)
        self.layout.addWidget(add_button)

        # Launch Software buttons
        self.layout.addWidget(QLabel('Launch Software:'))
        self.launch_layout = QVBoxLayout()
        self.layout.addLayout(self.launch_layout)

    def add_software(self):
        name = self.name_input.text()
        path = self.path_input.text()
        if name and path:
            self.software_entries[name] = path
            self.update_launch_buttons()
            self.name_input.clear()
            self.path_input.clear()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter both name and path.')

    def launch_software(self, name):
        path = self.software_entries.get(name)
        if path:
            try:
                import subprocess
                subprocess.Popen(path)
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to launch {name}. Error: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', f'No path found for {name}.')

    def update_launch_buttons(self):
        for i in reversed(range(self.launch_layout.count())):
            self.launch_layout.itemAt(i).widget().deleteLater()

        for name, _ in self.software_entries.items():
            launch_button = QToolButton()
            launch_button.setIcon(QIcon('icon.png'))  # Replace 'icon.png' with the path to your icon
            launch_button.setText(name)
            launch_button.setIconSize(128, 128)  # Set the icon size
            launch_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Set text under the icon
            launch_button.clicked.connect(lambda _, name=name: self.launch_software(name))
            self.launch_layout.addWidget(launch_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = SoftwareLauncher()
    launcher.show()
    sys.exit(app.exec_())
