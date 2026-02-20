import os
import threading
import subprocess
import json
from copy import deepcopy
from pathlib import Path
from PySide2.QtCore import Signal
from origin.dcc.common.utils.executables import set_executable


def pub_options_as_json(options):
    context = options["context_object"]

    if not isinstance(context, dict):
        as_dict = context.snapshot_session()

        new_options = deepcopy(options)
        new_options["context_object"] = as_dict
        options_json = json.dumps(new_options)

        return options_json

    as_json = json.dumps(options)
    return as_json


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

        self.dcc = self.options['dcc']
        self.set_script_to_run()

    def set_script_to_run(self):
        dev_root = Path(os.getenv("ORIGIN_ROOT"))
        batch_script_to_execute = Path(f"origin/dcc/extensions/{self.dcc}/batch/standalone.py")
        script_full_path = dev_root / batch_script_to_execute
        self.script_to_run = script_full_path.as_posix()

    def run(self):
        def batch_process():
            executable = set_executable(self.options)
            options_json = pub_options_as_json(self.options)

            command = [executable, self.script_to_run, "--task", self.task, "--options", options_json]

            print(f"\n*************************** BATCH INITIATED *********************************\n\n\n\n\n--------BATCH PROCESSING RUNNING WITH THESE OPTIONS:\n{options_json}\n\n\nAND THIS COMMAND:\n{command}\n\n\n" )

            try:
                self.process = subprocess.Popen(command,
                                                # check=True,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT,
                                                shell=False,
                                                text=True,
                                                bufsize=1
                                                )

                for line in self.process.stdout:
                    print(line, end="")

                for i, arg in enumerate(command):
                    print(f"{i}: {arg}")

                self.process.wait()
                print("RETURN CODE: ", self.process.returncode)

                if self.process.returncode != 0:
                    raise RuntimeError(
                        f"Batch job failed with return code {self.process.returncode}"
                    )

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

