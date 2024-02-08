import sys
from PySide2 import QtWidgets, QtGui
from database.entities.db_entities import DbPublish
from ui.slot_component_viewer_UI import SlotComponentsViewerUI


img_path = "/Users/arsithra/Documents/Learning_Python/PycharmProjects/Xchange/xcg_icons/play_icon_vsmall.png"

class SetReviewableComponent(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(SetReviewableComponent, self).__init__(parent)
        pic_video = QtGui.QPixmap(img_path)
        self.setIcon(pic_video)


class SlotComponentsViewerCore(SlotComponentsViewerUI):

    def __init__(self, slot_pub_id ='', slot_collection='', parent=None):
        super(SlotComponentsViewerCore, self).__init__(parent)
        self.slot_pub_id = slot_pub_id
        self.slot_collection = slot_collection

        self.populate_main_widget()


    def connect_to_slot(self, slot_func):
        cell_name = self.slot_component_viewer_tw.selectionModel().selectionChanged.connect(slot_func)
        return cell_name

    def get_selection_id(self):
        if self.slot_component_viewer_tw.selectedItems():
            cell_name = self.slot_component_viewer_tw.selectedItems()[6]
            return cell_name.text()


    def populate_main_widget(self):
        self.slot_component_viewer_tw.setRowCount(0)

        get_components = DbPublish().get_db_values(self.slot_collection, self.slot_pub_id, "components")
        if not get_components == None:
            rows_cnt = len(get_components)
            self.slot_component_viewer_tw.setRowCount(rows_cnt)
            cnt = 0
            for name, values in get_components.items():
                self.populate_publishes(str(name), str(values), cnt)
                cnt += 1
            return get_components

    def populate_publishes(self, name, value, row):
        self.component_name_btn = QtWidgets.QPushButton()
        self.component_path_le = QtWidgets.QLineEdit()
        self.open_btn = QtWidgets.QPushButton('Open')

        try:
            self.component_name_btn.setText(name)
            self.component_name_btn.setEnabled(False)
            self.component_path_le.setText(value)

        except:
            pass

        self.slot_component_viewer_tw.setCellWidget(row, 0, self.component_name_btn)
        self.slot_component_viewer_tw.setCellWidget(row, 1, self.component_path_le)
        self.slot_component_viewer_tw.setCellWidget(row, 2, self.open_btn)



if __name__ == "__main__":


    app = QtWidgets.QApplication(sys.argv)
    pub_id = 'Test.assets.characters.red_hulk.surfacing.look_dev.v0001'
    sl_collection = 'publish_slots_surfacing'
    test_dialog = SlotComponentsViewerCore(slot_pub_id=pub_id, slot_collection=sl_collection)

    test_dialog.show()
    sys.exit(app.exec_())