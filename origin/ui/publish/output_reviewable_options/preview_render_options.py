from PySide2 import QtWidgets, QtCore


class PreviewOptions(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PreviewOptions, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def reinitialize(self, pub_options=None):
        pass

    def create_widgets(self):
        self.preview_options_lb = QtWidgets.QLabel("Preview Options")
        self.playblast_chk = QtWidgets.QRadioButton("Playblast")
        self.render_chk = QtWidgets.QRadioButton("Render Turntable")
        self.no_preview_chk = QtWidgets.QRadioButton("No Preview")


    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.preview_options_lb)
        self.main_layout.addWidget(self.playblast_chk)
        self.main_layout.addWidget(self.render_chk)
        self.main_layout.addWidget(self.no_preview_chk)
        self.main_layout.addStretch()

    def create_connections(self):
        pass

    def get_checked(self):
        get_checked_widgets = []
        for idx in range(self.main_layout.count()):
            widget = self.main_layout.itemAt(idx).widget()

            if isinstance(widget, QtWidgets.QRadioButton):
                if widget.isChecked():
                    get_checked_widgets.append(widget)
        return get_checked_widgets

    def get_selected_options(self):
        checked_widgets = self.get_checked()
        wdg_names = [name.text().lower() for name in checked_widgets]
        if len(wdg_names) != 0:
            return {"review_medium": wdg_names[0]}
        return {"review_medium": ''}


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = PreviewOptions()

    test_dialog.show()
    sys.exit(app.exec_())
