import sys
from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QLineEdit


class PublishDialog(QDialog):
    def __init__(self, data, parent=None):
        super(PublishDialog, self).__init__(parent)
        self.setWindowTitle("Publish Dialog")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Publishing completed!"))

        # Access gathered data
        print("Final data:", data)

        publish_button = QPushButton("Publish")
        publish_button.clicked.connect(self.accept)
        self.layout().addWidget(publish_button)


class ThumbnailDialog(QDialog):
    def __init__(self, data, parent=None):
        super(ThumbnailDialog, self).__init__(parent)
        self.setWindowTitle("Thumbnail Dialog")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Thumbnail captured!"))

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.accept)
        self.layout().addWidget(next_button)


class CommentDialog(QDialog):
    def __init__(self, data, parent=None):
        super(CommentDialog, self).__init__(parent)
        self.setWindowTitle("Comment Dialog")
        self.setLayout(QVBoxLayout())
        self.data = data

        self.comment_edit = QLineEdit()
        self.layout().addWidget(QLabel("Enter Comments:"))
        self.layout().addWidget(self.comment_edit)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_dialog)
        self.layout().addWidget(next_button)

    def next_dialog(self):
        self.data['comments'] = self.comment_edit.text()
        self.accept()
        thumbnail_dialog = ThumbnailDialog(self.data, self)
        thumbnail_dialog.exec_()


class CheckDialog(QDialog):
    def __init__(self, data, parent=None):
        super(CheckDialog, self).__init__(parent)
        self.setWindowTitle("Check Dialog")
        self.setLayout(QVBoxLayout())
        self.data = data

        self.check_edit = QLineEdit()
        self.layout().addWidget(QLabel("Enter Checks:"))
        self.layout().addWidget(self.check_edit)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_dialog)
        self.layout().addWidget(next_button)

    def next_dialog(self):
        self.data['checks'] = self.check_edit.text()
        self.accept()
        comment_dialog = CommentDialog(self.data, self)
        comment_dialog.exec_()


class ContextDialog(QDialog):
    def __init__(self):
        super(ContextDialog, self).__init__()
        self.setWindowTitle("Context Dialog")
        self.setLayout(QVBoxLayout())

        self.data = {}

        self.context_edit = QLineEdit()
        self.layout().addWidget(QLabel("Enter Context:"))
        self.layout().addWidget(self.context_edit)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_dialog)
        self.layout().addWidget(next_button)

    def next_dialog(self):
        self.data['context'] = self.context_edit.text()
        self.accept()
        check_dialog = CheckDialog(self.data, self)
        check_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    context_dialog = ContextDialog()
    context_dialog.show()
    sys.exit(app.exec_())
