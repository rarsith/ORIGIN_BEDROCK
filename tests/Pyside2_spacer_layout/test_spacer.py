import sys
from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QWidget, QSpacerItem, QSizePolicy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        left_label = QLabel("Left Widget")
        right_label = QLabel("Right Widget")

        # Create spacer items
        left_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add widgets and spacers to the layout
        layout.addWidget(left_label)
        layout.addItem(left_spacer)
        layout.addWidget(right_label)
        layout.addItem(right_spacer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 400, 200)  # Set initial window size
    window.show()
    sys.exit(app.exec_())
