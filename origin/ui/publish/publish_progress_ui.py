import subprocess

from PySide2 import QtWidgets, QtCore


class ProgressWidget(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Batch Process Progress")
        self.setGeometry(300, 300, 400, 300)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.log_output = QtWidgets.QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)

        # Add widgets to layout
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.log_output)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)

        # Cancel button behavior
        self.cancel_button.clicked.connect(self.cancel_process)

        # Process variables
        self.thread = None

    def start_process(self, command):
        # Start the worker thread for the subprocess
        self.thread = ProcessThread(command)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.log_signal.connect(self.append_log)
        self.thread.finished.connect(self.on_process_complete)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def append_log(self, text):
        self.log_output.append(text)

    def on_process_complete(self):
        self.append_log("Process completed.")
        self.cancel_button.setText("Close")
        self.cancel_button.clicked.disconnect()
        self.cancel_button.clicked.connect(self.close)

    def cancel_process(self):
        if self.thread:
            self.thread.terminate_process()
            self.append_log("Process canceled.")
        self.close()


class ProcessThread(QtCore.QThread):
    progress_signal = QtCore.Signal(int)
    log_signal = QtCore.Signal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )

            for i, line in enumerate(self.process.stdout):
                self.log_signal.emit(line.strip())
                progress = min(100, (i + 1) * 10)  # Example progress calculation
                self.progress_signal.emit(progress)

            self.process.wait()
        except Exception as e:
            self.log_signal.emit(f"Error: {e}")
        finally:
            self.progress_signal.emit(100)

    def terminate_process(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()

