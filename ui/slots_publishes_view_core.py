from PySide2 import QtWidgets, QtGui

from ui.slots_publishes_view_UI import SlotsPublishesViewUI
from database.db_statuses import DbStatuses
from database.entities.db_entities import DbPublish
from database.utils.db_q_entity import DbReferences

img_path = "../icons/play_icon_vsmall.png"

class SetReviewableComponent(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(SetReviewableComponent, self).__init__(parent)
        pic_video = QtGui.QPixmap(img_path)
        self.setIcon(pic_video)


class SlotPublishesViewCore(SlotsPublishesViewUI):

    def __init__(self, main_pub_id = '', parent=None):
        super(SlotPublishesViewCore, self).__init__(parent)

        self.main_pub_id = main_pub_id

        self.return_pub_id()
        self.get_published_slots_ids()
        self.populate_main_widget()


    def show_name(self):
        return

    def return_pub_id(self):
        return (self.main_pub_id)

    def get_published_slots_ids(self):
        slot_pub_ids = DbReferences().get_db_referenced_attr('publishes', self.main_pub_id, 'publishing_slots', '_id')
        return slot_pub_ids

    def get_selection_id(self):
        if self.slot_publish_view_tw.selectedItems():
            cell_name = self.slot_publish_view_tw.selectedItems()[7]
            return cell_name.text()

    def get_selection_collection(self):
        if self.slot_publish_view_tw.selectedItems():
            cell_name = self.slot_publish_view_tw.selectedItems()[8]
            return cell_name.text()

    def connect_to_slot(self, slot_func):
        cell_name = self.slot_publish_view_tw.selectionModel().selectionChanged.connect(slot_func)
        return cell_name


    def populate_main_widget(self):

        self.slot_publish_view_tw.setRowCount(0)
        get_publish_id = DbReferences().get_db_referenced_attr('publishes', self.main_pub_id, 'publishing_slots', '_id')
        if not get_publish_id == None:
            rows_cnt = len(get_publish_id)
            self.slot_publish_view_tw.setRowCount(rows_cnt)
            cnt = 0
            for name in get_publish_id:
                self.populate_publishes(str(name), cnt)
                cnt += 1
            return get_publish_id

    def populate_publishes(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)

        self.slot_publish_view_tw.setItem(row, 1, item)

        self.status_cb = QtWidgets.QComboBox()
        self.status_cb.addItems(DbStatuses().list_all())

        get_publish_collection = DbReferences().get_db_referenced_attr('publishes',
                                                  self.main_pub_id,
                                                  'publishing_slots',
                                                  'parent_collection')

        self.get_publish_collection = DbPublish().get_db_values(get_publish_collection[0], name, "parent_collection")
        self.get_publish_id = DbPublish().get_db_values(get_publish_collection[0], name, "_id")
        self.get_publish_name = DbPublish().get_db_values(get_publish_collection[0], name, "display_name")
        self.get_publish_version = DbPublish().get_db_values(get_publish_collection[0], name, "version")
        self.get_publish_version_origin = DbPublish().get_db_values(get_publish_collection[0], name, "version_origin")
        self.get_publish_task = DbPublish().get_db_values(get_publish_collection[0], name, "task_name")
        self.get_publish_user = DbPublish().get_db_values(get_publish_collection[0], name, "artist")
        self.get_publish_status = DbPublish().get_db_values(get_publish_collection[0], name, "status")
        self.get_publish_date = DbPublish().get_db_values(get_publish_collection[0], name, "date")
        self.get_publish_time = DbPublish().get_db_values(get_publish_collection[0], name, "time")

        try:
            self.status_cb.setCurrentText(self.get_publish_status)
        except:
            pass

        self.slot_publish_view_tw.setCellWidget(row, 0, SetReviewableComponent(self))
        self.slot_publish_view_tw.setItem(row, 1, QtWidgets.QTableWidgetItem(self.get_publish_name))
        self.slot_publish_view_tw.setItem(row, 2, QtWidgets.QTableWidgetItem(self.get_publish_version))
        self.slot_publish_view_tw.setItem(row, 3, QtWidgets.QTableWidgetItem(self.get_publish_task))
        self.slot_publish_view_tw.setCellWidget(row, 4, self.status_cb)
        self.slot_publish_view_tw.setItem(row, 5, QtWidgets.QTableWidgetItem(self.get_publish_version_origin))
        self.slot_publish_view_tw.setItem(row, 6, QtWidgets.QTableWidgetItem(self.get_publish_user))
        self.slot_publish_view_tw.setItem(row, 7, QtWidgets.QTableWidgetItem(str(self.get_publish_date)))
        self.slot_publish_view_tw.setItem(row, 8, QtWidgets.QTableWidgetItem(str(self.get_publish_time)))
        self.slot_publish_view_tw.setItem(row, 9, QtWidgets.QTableWidgetItem(str(self.get_publish_id)))
        self.slot_publish_view_tw.setItem(row, 10, QtWidgets.QTableWidgetItem(str(self.get_publish_collection)))




if __name__ == "__main__":
    import sys
    from envars.envars import Envars

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "red_hulk"
    Envars.task_name = "modeling"

    app = QtWidgets.QApplication(sys.argv)
    pub_id = "Test.assets.characters.red_hulk.modeling.main_pub.v0007"
    test_dialog = SlotPublishesViewCore(main_pub_id=pub_id)




    # test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())