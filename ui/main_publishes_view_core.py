from PySide2 import QtWidgets, QtGui
from database.db_statuses import DbStatuses
from database.entities.db_entities import DbPublish
from ui.main_publishes_view_UI import MainPublishesViewUI

img_path = "../icons/play_icon_vsmall.png"

class SetReviewableComponent(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(SetReviewableComponent, self).__init__(parent)
        pic_video = QtGui.QPixmap(img_path)
        self.setIcon(pic_video)


class MainPublishesViewCore(MainPublishesViewUI):
    def __init__(self, parent=None):
        super(MainPublishesViewCore, self).__init__(parent)

        self.populate_main_widget()
        self.create_connections()

    def create_connections(self):
        self.refresh_btn.clicked.connect(self.populate_main_widget)

    def connect_to_slot(self, slot_func):
        cell_name = self.publish_view_tw.selectionModel().selectionChanged.connect(slot_func)
        return cell_name

    def get_selection_id(self):
        if self.publish_view_tw.selectedItems():
            cell_name = self.publish_view_tw.selectedItems()[6]
            return cell_name.text()


# PublishSlotsWidget -- START
    def get_value_of(self, slot):
        publishes = DbPublish().get_db_publishes_ids("publishes")
        return publishes

    def populate_main_widget(self):
        self.publish_view_tw.setRowCount(0)
        get_publish_id = DbPublish().get_db_publishes_ids("publishes")

        if not get_publish_id == None:
            rows_cnt = len(get_publish_id)
            self.publish_view_tw.setRowCount(rows_cnt)
            cnt = 0
            for name in get_publish_id:
                self.populate_publishes(name, cnt)
                cnt += 1
            return get_publish_id

    def populate_publishes(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)

        self.publish_view_tw.setItem(row, 2, item)

        self.status_cb = QtWidgets.QComboBox()
        self.status_cb.addItems(DbStatuses().list_all())
        self.status_cb.setStyleSheet('font-size: 8px;' 'font-family: "Rubik";')

        self.get_id = DbPublish().get_db_values("publishes", name, "_id")
        self.get_publish_name = DbPublish().get_db_values("publishes", name, "display_name")
        self.get_publish_version = DbPublish().get_db_values("publishes", name, "version")
        self.get_publish_task = DbPublish().get_db_values("publishes", name, "task_name")
        self.get_publish_user = DbPublish().get_db_values("publishes", name, "artist")
        self.get_publish_status = DbPublish().get_db_values("publishes", name, "status")
        self.get_publish_date = DbPublish().get_db_values("publishes", name, "date")
        self.get_publish_time = DbPublish().get_db_values("publishes", name, "time")

        try:
            self.status_cb.setCurrentText(self.get_publish_status)
        except:
            pass

        self.publish_view_tw.setItem(row, 0, QtWidgets.QTableWidgetItem(self.get_publish_name))
        self.publish_view_tw.setItem(row, 1, QtWidgets.QTableWidgetItem(self.get_publish_version))
        self.publish_view_tw.setItem(row, 2, QtWidgets.QTableWidgetItem(self.get_publish_task))
        self.publish_view_tw.setCellWidget(row, 3, self.status_cb)
        self.publish_view_tw.setItem(row, 4, QtWidgets.QTableWidgetItem(self.get_publish_user))
        self.publish_view_tw.setItem(row, 5, QtWidgets.QTableWidgetItem(str(self.get_publish_date)))
        self.publish_view_tw.setItem(row, 6, QtWidgets.QTableWidgetItem(str(self.get_publish_time)))
        self.publish_view_tw.setItem(row, 7, QtWidgets.QTableWidgetItem(str(self.get_id)))

    def insert_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        self.setItem(row, column, item)

    def get_published_status(self):
        version_status = self.get_value_of("status")
        return version_status



if __name__ == "__main__":
    import sys
    from envars.envars import Envars

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "red_hulk"
    Envars.task_name = "modeling"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = MainPublishesViewCore()
    # test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())