import sys
import time
import os
from PySide2.QtCore import QTimer, QTime, Qt, QEvent
from PySide2.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from PySide2.QtGui import QCloseEvent


class MoneyCounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Variables
        self.amount_per_hour = 60
        self.inactivity_timeout = 300000  # Default to 5 minutes (in milliseconds)
        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.timeout.connect(self.check_inactivity)
        self.inactivity_timer.start(1000)  # Check inactivity every second

        self.elapsed_time = QTime(0, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_money)

        self.last_active_time = time.time()
        self.log_file = "money_log.txt"
        self.is_timer_running = False

    def init_ui(self):
        # Inputs
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount per hour")

        self.inactivity_input = QLineEdit()
        self.inactivity_input.setPlaceholderText("Inactivity timeout (min)")

        # Labels
        self.time_label = QLabel("Time: 00:00")
        self.money_label = QLabel("Money: $0.00")

        # Buttons
        self.start_stop_button = QPushButton("Start Timer")
        self.start_stop_button.clicked.connect(self.toggle_timer)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)

        # Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Amount per hour:"))
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(QLabel("Inactivity timeout (min):"))
        input_layout.addWidget(self.inactivity_input)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.start_stop_button)
        control_layout.addWidget(self.reset_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.money_label)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Money Counter")

    def toggle_timer(self):
        if self.is_timer_running:
            self.timer.stop()
            self.start_stop_button.setText("Start Timer")
            self.is_timer_running = False
        else:
            try:
                self.amount_per_hour = float(self.amount_input.text())
                self.inactivity_timeout = int(self.inactivity_input.text()) * 60 * 1000
            except ValueError:
                self.amount_input.setText("Invalid input!")
                self.inactivity_input.setText("Invalid input!")
                return

            self.is_timer_running = True
            self.timer.start(60000)  # Update money every minute
            self.start_stop_button.setText("Stop Timer")
            self.last_active_time = time.time()  # Reset inactivity timer

    def update_money(self):
        self.elapsed_time = self.elapsed_time.addSecs(60)
        minutes_elapsed = self.elapsed_time.minute() + self.elapsed_time.hour() * 60
        money_earned = (self.amount_per_hour / 60) * minutes_elapsed

        self.time_label.setText(f"Time: {self.elapsed_time.toString('hh:mm')}")
        self.money_label.setText(f"Money: ${money_earned:.2f}")

        # Log each minute's earnings
        with open(self.log_file, "a") as log:
            log.write(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Time: {self.elapsed_time.toString('hh:mm')} - Money: ${money_earned:.2f}\n")

    def reset(self):
        self.timer.stop()
        self.is_timer_running = False
        self.elapsed_time = QTime(0, 0)
        self.time_label.setText("Time: 00:00")
        self.money_label.setText("Money: $0.00")
        self.start_stop_button.setText("Start Timer")

        # Clear log file on reset
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def check_inactivity(self):
        # Stop timer if inactivity period is reached
        if time.time() - self.last_active_time >= self.inactivity_timeout / 1000 and self.is_timer_running:
            self.toggle_timer()

    def event(self, event: QEvent):
        # Detect user activity and reset inactivity timer
        if event.type() in (QEvent.MouseMove, QEvent.KeyPress):
            print("ACTIVITY RECORDED")
            self.last_active_time = time.time()
        return super().event(event)

    def closeEvent(self, event: QCloseEvent):
        # Ensure the timer stops when the app closes
        self.timer.stop()
        self.inactivity_timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoneyCounterApp()
    window.show()
    sys.exit(app.exec_())
