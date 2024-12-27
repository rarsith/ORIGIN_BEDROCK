import os
import json

from PySide2 import QtCore
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)

INITIAL_SETUP_KEY = "INITIAL_SETUP_DONE"
MANDATORY_ENVARS = ["PROJECT_PATH", "ASSET_LIBRARY"]


class EnvarManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Environment Variable Manager")
        self.setGeometry(300, 200, 600, 400)

        self.init_ui()
        self.load_environment_variables()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Environment Variable Table
        self.env_table = QTableWidget()
        self.env_table.setColumnCount(2)
        self.env_table.setHorizontalHeaderLabels(["Variable", "Value"])
        self.env_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.env_table)

        # Buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_envar)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_envar)
        button_layout.addWidget(self.remove_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_environment_variables)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_environment_variables(self):
        """Load environment variables into the table."""
        self.env_table.setRowCount(0)

        # Load mandatory environment variables
        for var in MANDATORY_ENVARS:
            value = os.environ.get(var, "")
            self.add_table_row(var, value, mandatory=True)

        # Load custom environment variables
        for var, value in os.environ.items():
            if var not in MANDATORY_ENVARS and var != INITIAL_SETUP_KEY:
                self.add_table_row(var, value)

    def add_table_row(self, var_name, var_value, mandatory=False):
        """Add a row to the environment variable table."""
        row_position = self.env_table.rowCount()
        self.env_table.insertRow(row_position)

        var_item = QTableWidgetItem(var_name)
        var_item.setFlags(var_item.flags() & ~QtCore.Qt.ItemIsEditable if mandatory else var_item.flags())
        self.env_table.setItem(row_position, 0, var_item)

        value_item = QTableWidgetItem(var_value)
        self.env_table.setItem(row_position, 1, value_item)

    def add_envar(self):
        """Add a new custom environment variable."""
        self.add_table_row("NEW_VAR", "")

    def remove_envar(self):
        """Remove the selected environment variable."""
        selected_rows = set(index.row() for index in self.env_table.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            var_name = self.env_table.item(row, 0).text()
            if var_name in MANDATORY_ENVARS:
                QMessageBox.warning(self, "Error", f"Cannot remove mandatory variable: {var_name}")
            else:
                self.env_table.removeRow(row)

    def save_environment_variables(self):
        """Save the environment variables to the system."""
        for row in range(self.env_table.rowCount()):
            var_name = self.env_table.item(row, 0).text()
            var_value = self.env_table.item(row, 1).text()
            os.environ[var_name] = var_value

        os.environ[INITIAL_SETUP_KEY] = "1"  # Mark initial setup as done
        QMessageBox.information(self, "Saved", "Environment variables have been saved.")

    def initial_setup_check(self):
        """Check if the initial setup has been run."""
        return os.environ.get(INITIAL_SETUP_KEY) == "1"


if __name__ == "__main__":
    app = QApplication([])
    window = EnvarManagerUI()
    if not os.environ.get(INITIAL_SETUP_KEY):
        QMessageBox.information(window, "Initial Setup", "Running initial setup for environment variables.")
    window.show()
    app.exec_()
