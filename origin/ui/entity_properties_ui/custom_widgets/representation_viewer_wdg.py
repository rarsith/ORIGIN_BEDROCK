from PySide2 import QtWidgets

from origin.ui.entity_properties_ui.custom_widgets.representation_summary_wdg import EntitySummaryInfo
from origin.ui.entity_properties_ui.custom_widgets.representation_thumbnail_wdg import ThumbnailViewer


class RepresentationViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RepresentationViewer, self).__init__(parent)

        self.setMinimumHeight(150)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.thumbnail_wdg = ThumbnailViewer()
        self.entity_summary_wdg = EntitySummaryInfo()

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.thumbnail_wdg)
        main_layout.addWidget(self.entity_summary_wdg)

if __name__ == "__main__":
    import sys

    APP_CONFIG_FILE = r"/dcc/icons/movie_pic.png"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = RepresentationViewer()

    test_dialog.show()
    sys.exit(app.exec_())