import sys
import json
from PySide2 import QtWidgets

class UserModel:
    def __init__(self):
        self._username = ""
        self._email = ""

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    def to_dict(self):
        return {"username": self._username, "email": self._email}

    def from_dict(self, data):
        self._username = data.get("username", "")
        self._email = data.get("email", "")

class UserViewModel:
    def __init__(self, model):
        self._model = model
        self._users = []

    @property
    def users(self):
        return self._users

    @property
    def selected_user(self):
        return self._model

    def add_user(self):
        new_user = UserModel()
        self._users.append(new_user)

    def delete_user(self, user):
        self._users.remove(user)

    def save_to_json(self, filename):
        data = {"users": [user.to_dict() for user in self._users]}
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            self._users = [UserModel().from_dict(user_data) for user_data in data["users"]]

class UserView(QtWidgets.QWidget):
    def __init__(self, view_model):
        super().__init__()
        self._view_model = view_model

        self.user_list = QtWidgets.QListWidget(self)
        self.username_edit = QtWidgets.QLineEdit(self)
        self.email_edit = QtWidgets.QLineEdit(self)
        self.add_button = QtWidgets.QPushButton("Add User", self)
        self.delete_button = QtWidgets.QPushButton("Delete User", self)
        self.save_button = QtWidgets.QPushButton("Save", self)
        self.load_button = QtWidgets.QPushButton("Load", self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.user_list)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

        self.user_list.itemSelectionChanged.connect(self._on_user_selected)
        self.username_edit.textChanged.connect(self._on_username_changed)
        self.email_edit.textChanged.connect(self._on_email_changed)
        self.add_button.clicked.connect(self._on_add_clicked)
        self.delete_button.clicked.connect(self._on_delete_clicked)
        self.save_button.clicked.connect(self._on_save_clicked)
        self.load_button.clicked.connect(self._on_load_clicked)

        self._populate_user_list()

    def _populate_user_list(self):
        self.user_list.clear()
        for user in self._view_model.users:
            item = QtWidgets.QListWidgetItem(user.username)
            self.user_list.addItem(item)

    def _on_user_selected(self):
        selected_item = self.user_list.currentItem()
        if selected_item:
            index = self.user_list.row(selected_item)
            selected_user = self._view_model.users[index]
            self.username_edit.setText(selected_user.username)
            self.email_edit.setText(selected_user.email)

    def _on_username_changed(self, text):
        self._view_model.selected_user.username = text
        self._populate_user_list()

    def _on_email_changed(self, text):
        self._view_model.selected_user.email = text

    def _on_add_clicked(self):
        self._view_model.add_user()
        self._populate_user_list()

    def _on_delete_clicked(self):
        selected_item = self.user_list.currentItem()
        if selected_item:
            index = self.user_list.row(selected_item)
            selected_user = self._view_model.users[index]
            self._view_model.delete_user(selected_user)
            self._populate_user_list()

    def _on_save_clicked(self):
        self._view_model.save_to_json("user_data.json")

    def _on_load_clicked(self):
        self._view_model.load_from_json("user_data.json")
        self._populate_user_list()

def main():
    app = QtWidgets.QApplication(sys.argv)

    model = UserModel()
    view_model = UserViewModel(model)
    view = UserView(view_model)
    view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()