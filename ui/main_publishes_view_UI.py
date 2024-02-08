from PySide2 import QtWidgets


class MainPublishesViewWidgetBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(MainPublishesViewWidgetBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setColumnCount(8)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setColumnWidth(0, 120)
        self.setColumnWidth(1, 40)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 55)
        self.setColumnWidth(5, 60)
        self.setColumnWidth(6, 40)
        self.setColumnWidth(7, 0)

        self.setMinimumWidth(500)
        # self.setMaximumWidth(500)
        self.setSortingEnabled(True)



        for row in range(self.rowCount()):
            self.setRowHeight(row, 20)

        # self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(['Publish Name',
                                        'Version',
                                        'Task',
                                        'Status',
                                        'User',
                                        'Date',
                                        'Time',
                                        'Id',
                                        ])

class MainPublishesViewUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainPublishesViewUI, self).__init__(parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.publish_view_tw = MainPublishesViewWidgetBuild()

        self.search_le = QtWidgets.QLineEdit()
        self.search_le.setPlaceholderText("Search")

        self.refresh_btn = QtWidgets.QPushButton("Refresh")

        self.filter_menu_btn = QtWidgets.QPushButton("Custom_Filters")

        self.go_to_first_page_btn = QtWidgets.QPushButton("<<")
        self.go_to_first_page_btn.setFixedSize(30, 20)

        self.go_to_prev_page_btn = QtWidgets.QPushButton("<")
        self.go_to_prev_page_btn.setFixedSize(30, 20)

        self.go_to_next_page_btn = QtWidgets.QPushButton(">")
        self.go_to_next_page_btn.setFixedSize(30, 20)

        self.go_to_last_page_btn = QtWidgets.QPushButton(">>")
        self.go_to_last_page_btn.setFixedSize(30, 20)

        self.show_amount_le = QtWidgets.QLineEdit("50")
        self.show_amount_le.setFixedSize(50, 20)

        self.show_total_pages_le = QtWidgets.QLineEdit()
        self.show_total_pages_le.setFixedSize(50, 20)

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.search_le)
        top_layout.addWidget(self.refresh_btn)
        top_layout.addWidget(self.filter_menu_btn)


        bottom_btn_layout =  QtWidgets.QHBoxLayout()
        bottom_btn_layout.addStretch(1)
        bottom_btn_layout.addWidget(self.go_to_first_page_btn)
        bottom_btn_layout.addWidget(self.go_to_prev_page_btn)
        bottom_btn_layout.addWidget(self.show_total_pages_le)
        bottom_btn_layout.addWidget(self.show_amount_le)
        bottom_btn_layout.addWidget(self.go_to_next_page_btn)
        bottom_btn_layout.addWidget(self.go_to_last_page_btn)


        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.addLayout(bottom_btn_layout)

        slot_view_layout = QtWidgets.QHBoxLayout()
        slot_view_layout.addWidget(self.publish_view_tw)



        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(slot_view_layout)
        main_layout.addLayout(bottom_layout)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = MainPublishesViewUI()
    test_dialog.show()
    sys.exit(app.exec_())