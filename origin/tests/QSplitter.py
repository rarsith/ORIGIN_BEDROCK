import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QSplitter, QHBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Splitter Example')
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        text_edit_left = QTextEdit()
        text_edit_right = QTextEdit()

        # Create a splitter
        splitter = QSplitter()

        # Add widgets to the splitter
        splitter.addWidget(text_edit_left)
        splitter.addWidget(text_edit_right)

        # Set initial size for the left widget (adjust as needed)
        # splitter.setSizes([200, 400])

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 1)


        # Create a central widget and set the layout
        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
