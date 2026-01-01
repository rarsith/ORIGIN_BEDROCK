import os
import pprint
import threading
import subprocess
import json
from pathlib import Path
from PySide2.QtCore import Signal
from origin.dcc.executables import set_executable


class BatchProcessing:
    progress_signal = Signal(int)
    log_signal = Signal(str)

    def __init__(self, options, task):
        super().__init__()
        self.task = task
        self.options = options
        self.output_event = threading.Event()
        self.script_to_run = None
        self.output_data = None
        self.process = None

        self.dcc = os.getenv("DCC")
        self.set_script_to_run()

    def set_script_to_run(self):
        dev_root = Path(os.getenv("ORIGIN_ROOT"))
        batch_script_to_execute = Path(f"origin/dcc/{self.dcc}/batch/standalone.py")
        script_full_path = dev_root / batch_script_to_execute
        self.script_to_run = script_full_path.as_posix()

    def run(self):
        def batch_process():
            executable = set_executable()

            context = self.options["context_object"]
            as_dict = context.snapshot_session()
            new_options = self.options
            new_options["context_object"] = as_dict

            # Serialize the options dictionary into a JSON string
            options_json = json.dumps(new_options)
            print(options_json)

            # Construct the command
            command = [executable, self.script_to_run, "--task", self.task, "--options", options_json]
            print(command)

            try:
                # Capture the output of the subprocess
                self.process = subprocess.Popen(command,
                                                # check=True,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                shell=True,
                                                text=True
                                                )

                for line in self.process.stdout:
                    line = line.strip()
                    print(line)

                print(f"{self.dcc.capitalize()} batch job completed successfully.")

            except subprocess.CalledProcessError as e:
                print(f"Error occurred while running the {self.dcc.capitalize()} batch job: {e}")
                print("Batch Error Output:", e.stderr)
                return None
            except json.JSONDecodeError:
                print("Error decoding the frames output. Ensure the batch script outputs valid JSON.")
                return None

        thread = threading.Thread(target=batch_process)
        thread.start()

