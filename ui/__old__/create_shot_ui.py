import sys
from PySide2 import QtWidgets, QtCore

from database.entities.db_entities import DbAsset, DbProject
from envars.envars import Envars

class CreateShotUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateShotUI, self).__init__(parent)

        self.setWindowTitle("Create Shot")
        # self.setMinimumSize(550, 650)
        # self.setMaximumSize(550, 650)

        # self.setMinimumHeight(900)
        # self.setMaximumHeight(900)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_cb =  QtWidgets.QLabel()
        self.show_name_cb.setText(DbProject.current())

        self.shot_name_le = QtWidgets.QLineEdit()

        self.separator_top_lb = QtWidgets.QLabel("")
        self.shot_definition_lb =  QtWidgets.QLabel("-- Definition --")
        self.separator_bottom_lb = QtWidgets.QLabel("")

        self.preroll_le = QtWidgets.QLineEdit("10")

        self.motion_blur_high_le = QtWidgets.QLineEdit("0.25")
        self.motion_blur_low_le = QtWidgets.QLineEdit("-0.25")

        self.full_range_in_le = QtWidgets.QLabel()
        self.full_range_in_le.setText(self.compute_full_range_in())

        self.full_range_out_le = QtWidgets.QLabel()
        self.full_range_out_le.setText(self.compute_full_range_out())

        self.frame_rate_le = QtWidgets.QLineEdit("24")

        self.input_frame_in = QtWidgets.QLineEdit("1001")
        self.input_frame_out = QtWidgets.QLineEdit("1001")

        self.handles_head_le = QtWidgets.QLineEdit("8")
        self.handles_tail_le = QtWidgets.QLineEdit("8")

        self.cut_in_le = QtWidgets.QLabel()
        self.cut_in_le.setText(self.compute_cut_in_le())

        self.cut_out_le = QtWidgets.QLabel()
        self.cut_out_le.setText(self.compute_cut_out_le())

        self.shot_render_res_x_le = QtWidgets.QLineEdit()
        self.shot_render_res_x_le.setText(self.compute_res_x())

        self.shot_render_res_y_le = QtWidgets.QLineEdit()
        self.shot_render_res_y_le.setText(self.compute_res_y())

        self.retime_ckb = QtWidgets.QCheckBox()
        self.repo_ckb = QtWidgets.QCheckBox()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_cb)
        form_layout.addRow("Shot Name: ", self.shot_name_le)
        form_layout.setSpacing(5)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        definition_form_layout = QtWidgets.QFormLayout()
        definition_form_layout.addWidget(self.separator_top_lb)
        definition_form_layout.addWidget(self.shot_definition_lb)
        definition_form_layout.addWidget(self.separator_bottom_lb)
        definition_form_layout.addRow("Preroll: ", self.preroll_le)
        definition_form_layout.addRow("Input Frame In: ", self.input_frame_in)
        definition_form_layout.addRow("Input Frame Out: ", self.input_frame_out)
        definition_form_layout.addRow("Handles Head: ", self.handles_head_le)
        definition_form_layout.addRow("Handles Tail: ", self.handles_tail_le)
        definition_form_layout.addRow("Full Range In: ", self.full_range_in_le)
        definition_form_layout.addRow("Full Range Out: ", self.full_range_out_le)
        definition_form_layout.addRow("Edit Cut In: ", self.cut_in_le)
        definition_form_layout.addRow("Edit Cut Out: ", self.cut_out_le)
        definition_form_layout.addRow("Frame Rate: ", self.frame_rate_le)
        definition_form_layout.addRow("Motion Blur High: ", self.motion_blur_high_le)
        definition_form_layout.addRow("Motion Blur Low: ", self.motion_blur_low_le)

        resolution_layout = QtWidgets.QHBoxLayout()
        resolution_layout.addWidget(self.shot_render_res_x_le)
        resolution_layout.addWidget(self.shot_render_res_y_le)

        definition_form_layout.addRow("Render Resolution: ", resolution_layout)


        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(definition_form_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def create_connections(self):

        self.input_frame_in.textChanged[str].connect(self.compute_cut_in_le)
        self.input_frame_in.textChanged[str].connect(self.compute_scene_frame_in)
        self.handles_head_le.textChanged[str].connect(self.compute_scene_frame_in)

        self.input_frame_out.textChanged[str].connect(self.compute_cut_out_le)
        self.input_frame_out.textChanged[str].connect(self.compute_scene_frame_out)
        self.handles_tail_le.textChanged[str].connect(self.compute_scene_frame_out)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_seq(self):
        seq_text = self.parent_seq_cb.currentText()
        return seq_text

    def refresh_combo(self):
        self.parent_seq_cb.clear()

    def compute_cut_in_le(self):
        get_frame_in = self.input_frame_in.text()
        get_handles_head = self.handles_head_le.text()
        calculate_cut_in = int(get_frame_in) + int(get_handles_head)
        self.cut_in_le.setText(str(calculate_cut_in))
        return str(calculate_cut_in)

    def compute_cut_out_le(self):
        get_frame_out = self.input_frame_in.text()
        get_handles_tail = self.handles_tail_le.text()
        calculate_cut_out = int(get_frame_out) - int(get_handles_tail)
        self.cut_out_le.setText(str(calculate_cut_out))
        return str(calculate_cut_out)

    def compute_scene_frame_in(self):
        get_frame_in = self.input_frame_in.text()
        get_handles_head = self.handles_head_le.text()
        calculate_cut_in = int(get_frame_in) + int(get_handles_head)
        self.cut_in_le.setText(str(calculate_cut_in))
        return str(calculate_cut_in)

    def compute_scene_frame_out(self):
        get_frame_out = self.input_frame_out.text()
        get_handles_tail = self.handles_tail_le.text()
        calculate_cut_out = int(get_frame_out) - int(get_handles_tail)
        self.cut_out_le.setText(str(calculate_cut_out))
        return str(calculate_cut_out)

    def compute_res_x(self):
        return "from plate"

    def compute_res_y(self):
        return "from plate"

    def compute_full_range_out(self):
        return "ingest plate"

    def compute_full_range_in(self):
        return "ingest plate"

    def compute_definition(self):
        definition = {'full_range_in':self.full_range_in_le.text(),
                           'full_range_out':self.full_range_out_le.text(),
                           'frame_in': self.input_frame_in.text(),
                           'frame_out': self.input_frame_out.text(),
                           'handles_head': self.handles_head_le.text(),
                           'handles_tail': self.handles_tail_le.text(),
                           'preroll': self.preroll_le.text(),
                           'shot_type': self.shot_type_cb.currentText(),
                           'cut_in':self.cut_in_le.text(),
                           'cut_out':self.cut_out_le.text(),
                           'frame_rate': self.frame_rate_le.text(),
                           'motion_blur_high': self.motion_blur_high_le.text(),
                           'motion_blur_low': self.motion_blur_low_le.text(),
                           'res_x': self.shot_render_res_x_le.text(),
                           'res_y': self.shot_render_res_y_le.text()}
        return definition

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        DbAsset().create(self.shot_name_le.text())
        self.shot_name_le.clear()

    def get_shows(self):
        shows = DbProject().get_all()
        return shows


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    from envars.envars import Envars

    Envars.show_name = "Test"
    Envars.branch_name = "sequences"
    Envars.category = "GooGoo"
    Envars.entry_name = "GooGoo"
    Envars.task_name = "rigging"

    create_shot = CreateShotUI()
    create_shot.show()
    sys.exit(app.exec_())