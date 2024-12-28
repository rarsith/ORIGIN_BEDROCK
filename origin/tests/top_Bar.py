from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QColor


class CustomTitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        # Layout for the custom title bar
        layout = QHBoxLayout()

        # Label for the title bar
        self.label = QLabel("Custom Title Bar")
        layout.addWidget(self.label)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        # QSS for styling the custom title bar
        self.setStyleSheet("""
            QWidget {
                background-color: #4a90e2;  /* Title bar background color */
                color: white;  /* Text color */
                border: 1px solid #2c6f8c;
            }
            QLabel {
                font-weight: bold;
                padding-left: 10px;
            }
            QPushButton {
                background-color: #e74c3c;  /* Close button color */
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the custom title bar and make the window frameless
        self.setMenuWidget(CustomTitleBar())
        self.setWindowFlag(Qt.FramelessWindowHint)  # Makes the window frameless

        # Main content of the window
        self.setWindowTitle("Custom Title Bar Example")
        self.setGeometry(100, 100, 600, 400)

        # Initialize mouse dragging
        self._dragging = False
        self._drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
