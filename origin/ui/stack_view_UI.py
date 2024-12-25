from origin.ui.style.icons import OriginIcons
from origin.ui.style import buttons_styles as btns
from PySide2 import QtWidgets, QtCore, QtGui


class CustomDelegate(QtWidgets.QStyledItemDelegate):
    def sizeHint(self, option, index):
        size_hint = super().sizeHint(option, index)
        size_hint.setHeight(25)  # Set the desired row height here
        return size_hint


class StackViewWidgetBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(StackViewWidgetBuild, self).__init__(parent)

        # self.widget_width = 400
        self.widget_build()
        self.setItemDelegate(CustomDelegate())

    def widget_build(self):
        self.setColumnCount(12)
        width = 950

        # self.setHeaderHidden(True)
        header = self.header()
        header.setStretchLastSection(True)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        # self.setColumnCount(2)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)


        self.setHeaderLabels(['----',
                              'Publish Name',
                              'Version',
                              'Status',
                              'Asset Type',
                              'Task Type',
                              'Published by',
                              'Published',      # try to include date and time in the same cell
                              'Description',
                              "Id",             # hidden by default
                              "Parent Asset",   # hidden by default
                              "Has Notes"       # hidden by default
                              ])

        # self.widget_columns_names = ["Task", "Task Type"]
        # self.setColumnCount(len(self.widget_columns_names))
        # self.setHeaderLabels(self.widget_columns_names)

        self.setColumnWidth(0, round(width * 0.01))
        self.setColumnWidth(1, round(width * 0.255))
        self.setColumnWidth(2, round(width * 0.07))
        self.setColumnWidth(3, round(width * 0.12))
        self.setColumnWidth(4, round(width * 0.1))
        self.setColumnWidth(5, round(width * 0.1))
        self.setColumnWidth(6, round(width * 0.1))
        self.setColumnWidth(7, round(width * 0.12))
        self.setColumnWidth(8, round(width * 0.15))
        self.setColumnWidth(9, round(width * 0.08))
        self.setColumnWidth(10, round(width * 0.08))
        self.setColumnWidth(11, round(width * 0.08))
        self.setColumnWidth(12, round(width * 0.08))

        self.setUniformRowHeights(True)

        self.setColumnHidden(10, True)
        self.setColumnHidden(11, True)
        self.setColumnHidden(9, True)
        self.setColumnHidden(8, True)

        self.setSortingEnabled(True)
        self.sortItems(7, QtCore.Qt.DescendingOrder)


class StackViewUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StackViewUI, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

        self.publish_view_tw = StackViewWidgetBuild()

        self.search_le = QtWidgets.QLineEdit()
        self.search_le.setPlaceholderText("Search for Publish Name, Asset Type, Owner")

        self.save_changes_btn = QtWidgets.QPushButton()
        self.save_changes_btn.setIcon(OriginIcons().save_button_icon())
        self.save_changes_btn.setFixedSize(32, 32)
        self.save_changes_btn.setStyleSheet(btns.hover_orange)

        self.refresh_btn = QtWidgets.QPushButton()
        self.refresh_btn.setIcon(OriginIcons().refresh_button_icon())
        self.refresh_btn.setFixedSize(32, 32)
        self.refresh_btn.setStyleSheet(btns.hover_orange)

        self.filter_menu_btn = QtWidgets.QPushButton()
        self.filter_menu_btn.setIcon(OriginIcons().filter_button_icon())
        self.filter_menu_btn.setFixedSize(32, 32)
        self.filter_menu_btn.setStyleSheet(btns.hover_orange)

        self.go_to_first_page_btn = QtWidgets.QPushButton()
        self.go_to_first_page_btn.setIcon(OriginIcons().first_page_icon())
        self.go_to_first_page_btn.setFixedSize(32, 32)
        self.go_to_first_page_btn.setStyleSheet(btns.hover_orange)

        self.go_to_prev_page_btn = QtWidgets.QPushButton()
        self.go_to_prev_page_btn.setIcon(OriginIcons().previous_page_icon())
        self.go_to_prev_page_btn.setFixedSize(32, 32)
        self.go_to_prev_page_btn.setStyleSheet(btns.hover_orange)

        self.go_to_next_page_btn = QtWidgets.QPushButton()
        self.go_to_next_page_btn.setIcon(OriginIcons().next_page_icon())
        self.go_to_next_page_btn.setFixedSize(32, 32)
        self.go_to_next_page_btn.setStyleSheet(btns.hover_orange)

        self.go_to_last_page_btn = QtWidgets.QPushButton()
        self.go_to_last_page_btn.setIcon(OriginIcons().last_page_icon())
        self.go_to_last_page_btn.setFixedSize(32, 32)
        self.go_to_last_page_btn.setStyleSheet(btns.hover_orange)

        self.show_current_page_le = QtWidgets.QLineEdit("1")
        self.show_current_page_le.setFixedSize(50, 20)

        self.show_total_pages_le = QtWidgets.QLineEdit()
        self.show_total_pages_le.setFixedSize(50, 20)
        self.show_total_pages_le.setReadOnly(True)

        validator = QtGui.QIntValidator()
        self.load_limit_le = QtWidgets.QLineEdit("30")
        self.load_limit_le.setValidator(validator)
        self.load_limit_le.setFixedSize(50, 20)

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.save_changes_btn)
        top_layout.addWidget(self.refresh_btn)

        left_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        right_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.publish_view_tw)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = StackViewUI()
    test_dialog.show()
    sys.exit(app.exec_())