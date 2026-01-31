# doci_ui.py
import sys
import json
import time
from pathlib import Path

from PySide2.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar
)
from PySide2.QtCore import QTimer


WATCH_DIR = Path("dropbox")
STATE_FILE = Path("publish_state.json")


class PublishUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DOCI Publisher")
        self.resize(600, 300)

        layout = QVBoxLayout(self)

        self.publish_btn = QPushButton("Publish")
        self.publish_btn.clicked.connect(self.publish)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ["Task", "Status", "Progress"]
        )

        layout.addWidget(self.publish_btn)
        layout.addWidget(self.table)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(200)

    def publish(self):
        WATCH_DIR.mkdir(exist_ok=True)

        job = {
            "publish": "test_publish",
            "tasks": [
                "geometry_export",
                "playblast",
                "movie"
            ]
        }

        with open(WATCH_DIR / "publish.json", "w") as f:
            json.dump(job, f, indent=2)

    def refresh(self):
        if not STATE_FILE.exists():
            return

        with open(STATE_FILE) as f:
            state = json.load(f)

        self.table.setRowCount(len(state))

        for row, (task, info) in enumerate(state.items()):
            self.table.setItem(row, 0, QTableWidgetItem(task))
            self.table.setItem(row, 1, QTableWidgetItem(info["status"]))

            bar = QProgressBar()
            bar.setValue(info["progress"])
            self.table.setCellWidget(row, 2, bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = PublishUI()
    ui.show()
    sys.exit(app.exec_())
