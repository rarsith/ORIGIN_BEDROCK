import os
from PySide2 import QtGui

class OriginIcons:
    def __init__(self):
        self.icon_path = self._get_icons_path()

    def _get_dev_root(self):
        return os.getenv("ORIGIN_ROOT")

    def _get_icons_path(self):
        dev_root = self._get_dev_root()
        return os.path.join(dev_root, "ui/style/icons")

    def refresh_button_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "refresh_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def add_button_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "add_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def export_button_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "upgrade_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def save_button_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "save_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def filter_button_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "filter_alt_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def next_page_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "keyboard_arrow_right_48dp_FILL0_wght400_GRAD0_opsz48_32x32"))
        return icon

    def previous_page_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "keyboard_arrow_left_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def last_page_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "keyboard_double_arrow_right_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def first_page_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "keyboard_double_arrow_left_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon

    def play_icon(self):
        icon = QtGui.QIcon(os.path.join(self.icon_path, "play_arrow_48dp_FILL0_wght400_GRAD0_opsz48_32x32.png"))
        return icon
