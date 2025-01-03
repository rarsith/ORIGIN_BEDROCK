import os
import threading
import subprocess
import json


def run_maya_batch_script(script_path, options):
    # def batch_process():
        # maya_bin = os.getenv("MAYABIN")

    maya_bin = "E:/programs/Autodesk/Maya2024/bin"
    mayapy_executable = os.path.join(maya_bin, "mayapy.exe")
    mayapy_normalized = os.path.normpath(mayapy_executable)

    context = options["context_object"]
    as_dict = context.snapshot_session()
    new_options = options
    new_options["context_object"] = as_dict

    # Serialize the options dictionary into a JSON string
    options_json = json.dumps(new_options)

    # Construct the command
    command = [
        mayapy_normalized,
        script_path,
        "--options", options_json
    ]

    # startupinfo = None
    # if os.name == 'nt':  # Windows
    #     startupinfo = subprocess.STARTUPINFO()
    #     startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #     creationflags = subprocess.CREATE_NEW_CONSOLE
    # else:  # macOS/Linux
    #     creationflags = 0  # No additional flags for UNIX

    try:
        # Capture the output of the subprocess
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
            # creationflags=creationflags
        )

        # stdout, stderr = result.communicate()

        # for line in result.stdout:
        #     print(f"STDOUT: {line.strip()}")

        # Parse the output to extract frames
        output = result.stdout.strip()

        # result.wait()
        print("Maya batch job completed successfully.")
        return output

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the Maya batch job: {e}")
        print("Batch Error Output:", e.stderr)
        return None
    except json.JSONDecodeError:
        print("Error decoding the frames output. Ensure the batch script outputs valid JSON.")
        return None


    # thread = threading.Thread(target = batch_process)
    # thread.start()

# Example usage
# run_maya_batch_script("/origin/dcc/maya/batch/playblast/maya_make_playblast.py")
