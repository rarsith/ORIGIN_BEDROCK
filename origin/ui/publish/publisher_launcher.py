from PySide2 import QtWidgets
from origin.ui.publish.origin_publisher import OriginPublisher

if __name__ == "__main__":
    import sys

    qss_style_file = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\origin\ui\style\stylesheets\dark_orange\dark_orange_style.qss"

    app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    test_dialog = OriginPublisher()
    test_dialog.setWindowTitle("Publisher")
    test_dialog.setMinimumHeight(650)
    test_dialog.setMinimumWidth(450)

    test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())
