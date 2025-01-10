import os
import threading
import subprocess
import json
from pathlib import Path


class MayaBatchScript:
    def __init__(self, options, task):
        self.task = task
        self.options = options
        self.output_event = threading.Event()
        self.script_to_run = None
        self.output_data = None

        self.set_script_to_run()

    def set_script_to_run(self):
        dev_root = Path(os.getenv("ORIGIN_ROOT"))
        batch_script_to_execute = Path("origin/dcc/maya/batch/maya_standalone.py")
        script_full_path = dev_root / batch_script_to_execute
        self.script_to_run = script_full_path.as_posix()

    def run(self):
        def batch_process():
            maya_bin = Path(os.getenv("MAYABIN"))

            mayapy_executable = maya_bin / "mayapy.exe"
            mayapy_normalized = mayapy_executable.as_posix()

            context = self.options["context_object"]
            as_dict = context.snapshot_session()
            new_options = self.options
            new_options["context_object"] = as_dict

            # Serialize the options dictionary into a JSON string
            options_json = json.dumps(new_options)

            # Construct the command
            command = [mayapy_normalized, self.script_to_run, "--task", self.task, "--options", options_json]

            try:
                # Capture the output of the subprocess
                result = subprocess.run(command, check=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        text=True
                                        )

                output = result.stdout.strip()
                self.output_data = output
                self.output_event.set()

                print("Maya batch job completed successfully.")
                return output

            except subprocess.CalledProcessError as e:
                print(f"Error occurred while running the Maya batch job: {e}")
                print("Batch Error Output:", e.stderr)
                return None
            except json.JSONDecodeError:
                print("Error decoding the frames output. Ensure the batch script outputs valid JSON.")
                return None

        thread = threading.Thread(target=batch_process)
        thread.start()

        # self.output_event.wait()  # Block until the event is set (process completes)
        # return self.output_data  # Return the output once available
