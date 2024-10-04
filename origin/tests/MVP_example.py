import sys
from PySide2 import QtWidgets

# Model
class GreetingModel:
    def get_greeting(self, name):
        return f"Hello, {name}!"

# View
class GreetingView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVP Greeting App")

        self.name_input = QtWidgets.QLineEdit(self)
        self.greeting_label = QtWidgets.QLabel(self)
        self.greet_button = QtWidgets.QPushButton("Greet", self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Enter your name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.greet_button)
        layout.addWidget(self.greeting_label)
        self.setLayout(layout)

    def get_name(self):
        return self.name_input.text()

    def set_greeting(self, greeting):
        self.greeting_label.setText(greeting)

# Presenter
class GreetingPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.greet_button.clicked.connect(self.show_greeting)

    def show_greeting(self):
        name = self.view.get_name()
        greeting = self.model.get_greeting(name)
        self.view.set_greeting(greeting)

def main():
    app = QtWidgets.QApplication(sys.argv)
    model = GreetingModel()
    view = GreetingView()
    presenter = GreetingPresenter(model, view)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()