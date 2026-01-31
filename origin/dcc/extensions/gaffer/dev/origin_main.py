from master import MainUI

import GafferUI
from PySide2 import QtWidgets


class MyPySideWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Hello from PySide2!"))

# Create Gaffer window
gafferWindow = GafferUI.Window("Origin Master")

widget_add = MainUI()
widget_add.set_style()

# Add widget to the Gaffer window's layout
column = GafferUI.ListContainer(GafferUI.ListContainer.Orientation.Vertical)
column._qtWidget().layout().addWidget(widget_add)

gafferWindow.setChild(column)
gafferWindow.setVisible(True)