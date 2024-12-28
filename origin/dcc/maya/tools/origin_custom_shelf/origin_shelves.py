import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

# Function to get the main Maya window
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

# Custom Shelf Widget Class
class CustomShelfWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(CustomShelfWidget, self).__init__(parent)

        # Set window title and features
        self.setWindowTitle("Origin Tools Shelf")
        self.setFloating(False)  # Ensures it is dockable

        # Create the main widget and horizontal layout
        self.main_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout(self.main_widget)  # Horizontal layout
        
        self.button_layout = QtWidgets.QHBoxLayout()  # Layout for buttons
        self.layout.addLayout(self.button_layout)

        # Add context menu for shelf selection
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # Dictionary to hold shelf buttons
        self.shelves = {
            "Shelf 1": self.create_shelf(1),
            "Shelf 2": self.create_shelf(2),
            "Shelf 3": self.create_shelf(3)
        }

        # Initialize with the first shelf
        self.current_shelf_name = "Shelf 1"
        self.update_shelf(self.current_shelf_name)

        self.layout.addStretch()
        # Set the central widget of the dockable window
        self.setWidget(self.main_widget)

    def create_shelf(self, shelf_number):
        """ Create buttons for a specific shelf. """
        buttons = []
        for i in range(1, 26):  # 25 buttons for each shelf
            button = QtWidgets.QPushButton(f"Tool {i} (Shelf {shelf_number})")
            button.setFixedSize(40, 40)  # Set size similar to Maya shelf buttons
            button.clicked.connect(lambda _, tool=i: self.run_tool(tool, shelf_number))
            buttons.append(button)
        return buttons

    def update_shelf(self, shelf_name):
        """ Update the button layout to the specified shelf. """
        # Clear the current layout
        for i in reversed(range(self.button_layout.count())):
            widget = self.button_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Delete the old buttons
        
        # Add new buttons for the selected shelf
        self.current_shelf_name = shelf_name
        for button in self.shelves[shelf_name]:
            self.button_layout.addWidget(button)

    def show_context_menu(self, pos):
        """ Show the context menu for switching shelves. """
        menu = QtWidgets.QMenu(self)

        # Add options to switch between shelves
        for shelf_name in self.shelves.keys():
            action = menu.addAction(shelf_name)
            action.triggered.connect(lambda _, name=shelf_name: self.update_shelf(name))
        
        menu.exec_(self.mapToGlobal(pos))

    # Define actions for the buttons
    def run_tool(self, tool_number, shelf_number):
        print(f"Running Tool {tool_number} from Shelf {shelf_number}...")  # Replace with actual tool logic

    def open_settings_window(self):
        print("Opening settings window...")  # Replace with actual settings window logic

# Show the custom shelf widget
def show_custom_shelf():
    maya_main_window = get_maya_main_window()
    custom_shelf = CustomShelfWidget(parent=maya_main_window)

    # Add the custom shelf widget to the main Maya window
    custom_shelf.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Clean up on close
    custom_shelf.show()

# Call the function to display the custom shelf widget
show_custom_shelf()
