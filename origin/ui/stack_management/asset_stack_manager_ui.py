from PySide2 import QtWidgets, QtGui, QtCore

from origin.envars.origin_envars import ContextHandler


class DropEventFilter(QtCore.QObject):
    def __init__(self, list_widget, table_widget):
        super().__init__()
        self.list_widget = list_widget
        self.table_widget = table_widget

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Drop:
            pos = event.pos()
            row = self.table_widget.rowAt(pos.y())
            print(row)
            column = self.table_widget.columnAt(pos.x())
            print(column)

            # Ensure drop happens only at a valid cell
            if row == 0 and column == 0:
                item_text = self.list_widget.currentItem().text()
                self.table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem(item_text))
                self.table_widget.setAcceptDrops(False)
                return True
              # Event handled

        return super().eventFilter(source, event)


class StackTarget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(StackTarget, self).__init__(parent)

        self.setColumnCount(2)
        self.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)

        self.setShowGrid(False)
        vertical_header = self.verticalHeader()
        vertical_header.setDefaultSectionSize(2)
        vertical_header.hide()

        horizontal_header = self.horizontalHeader()
        horizontal_header.setMinimumHeight(2)
        horizontal_header.setMaximumHeight(3)
        horizontal_header.hide()

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.setAcceptDrops(False)
        self.setDragDropMode(QtWidgets.QTableWidget.DropOnly)
        self.setDropIndicatorShown(True)

        self.setRowCount(1)


class StackLoader(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(StackLoader, self).__init__(parent)

        self.setDragEnabled(False)


class AssetStackManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AssetStackManager, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.drop_filter = DropEventFilter(self.stack_loader_lw, self.stack_target_tw)
        self.stack_target_tw.viewport().installEventFilter(self.drop_filter)

    def create_widgets(self):
        self.stack_loader_lw = StackLoader()
        self.stack_loader_lw.addItems(["Item 1", "Item 2", "Item 3", "Item 4"])

        self.stack_target_tw = StackTarget()
        self.clear_target_btn = QtWidgets.QPushButton("Clear")
        self.create_btn = QtWidgets.QPushButton("Create Stack")
        self.remove_btn = QtWidgets.QPushButton("Delete Stack")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.stack_loader_lw)
        # top_layout.addWidget(self.stack_target_tw)

        buttons_layout = QtWidgets.QHBoxLayout()

        buttons_layout.addWidget(self.remove_btn)
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.clear_target_btn)
        buttons_layout.setAlignment(QtCore.Qt.AlignRight)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(buttons_layout)

        horizontal_splitter = QtWidgets.QSplitter()
        horizontal_splitter.setOrientation(QtCore.Qt.Horizontal)
        top_layout.addWidget(horizontal_splitter)

        horizontal_splitter.insertWidget(0, self.stack_loader_lw)
        # horizontal_splitter.insertWidget(1, self.stack_target_tw)
        horizontal_splitter.setSizes([100, 300])

    def create_connections(self):
        pass

    # def eventFilter(self, source, event):
    #     print(self.stack_target_tw.acceptDrops())
    #     if event.type() == QtCore.QEvent.Drop and self.stack_target_tw.acceptDrops():
    #         if event.source() == self.stack_loader_lw:
    #             # Get the drop position and determine the row and column
    #             pos = event.pos()
    #             row = self.stack_target_tw.rowAt(pos.y())
    #             print(row)
    #             column = self.stack_target_tw.columnAt(pos.x())
    #             print(column)
    #
    #             # Allow drops only in the first column (index 0)
    #             if row == 0 and column == 0:
    #                 item_text = self.stack_loader_lw.currentItem().text()
    #                 self.stack_target_tw.setItem(0, 0, QtWidgets.QTableWidgetItem(item_text))
    #                 self.stack_target_tw.setAcceptDrops(False)
    #                 return True
    #     return super().eventFilter(source, event)  #


class LoaderMainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LoaderMainUI, self).__init__(parent)
        self.setMinimumHeight(350)
        self.setMinimumWidth(500)
        self.central_widget = AssetStackManager()

        self.setWindowTitle(f"Asset Stack Manager")

        self.setCentralWidget(self.central_widget)
        self.show()


if __name__ == "__main__":
    import sys

    qss_style_file = "C:\\Users\\arsithra\\PycharmProjects\\ORIGIN_BEDROCK\\origin\\ui\\style\\stylesheets\\dark_orange\\dark_orange_style.qss"

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'tafer',
                      'entity_id': 'The_Rock.assets.chr.tafer',
                      'entity_type': 'asset',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "The_Rock.assets.chr.tafer.modeling",
                      'db_asset_id': 'The_Rock.assets.chr.tafer.geometry.tafer',
                      'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer',
                      }

    context_obj = ContextHandler()
    context_obj.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = LoaderMainUI()

    with open(qss_style_file, "r") as f:
        _style = f.read()
        test_dialog.setStyleSheet(_style)

    # test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())