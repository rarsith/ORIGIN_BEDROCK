import subprocess
import os


# --- SETTINGS ---
PIPELINE_ROOT = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK"
# Make sure this path is where origin_server.py is actually located
SERVER_DIR = os.path.join(PIPELINE_ROOT, "origin", "server")
PYTHON_310 = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\venv\Scripts\python.exe"

def launch():
    print("--- STARTING ORIGIN PIPELINE SERVER ---")

    # 1. Start the Server in the background
    # Note: We use the directory where origin_server.py lives as the 'cwd' (current working directory)
    # so uvicorn can find the file.
    server_process = subprocess.Popen(
        [PYTHON_310, "-m", "uvicorn", "origin_server:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=SERVER_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print("Bridge Server is running in a separate window.")
    print("Close the server window or press Ctrl+C in this terminal to stop.")

    try:
        # 2. This is the key! This prevents the script from finishing.
        # It will 'hang' here as long as the server window is open.
        server_process.wait()
    except KeyboardInterrupt:
        # If you press Ctrl+C in your main terminal, shut the server down nicely
        print("\nShutting down Bridge Server...")
        server_process.terminate()

if __name__ == "__main__":
    launch()