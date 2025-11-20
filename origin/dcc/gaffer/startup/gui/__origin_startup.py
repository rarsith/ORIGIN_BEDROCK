# import os
# import sys

# # Example: Adding a custom path to sys.path
# custom_path = os.path.join(os.getenv("ORIGIN_ROOT"), "custom_modules")
# sys.path.append(custom_path)

# Example: Import and execute your script
# script_path = os.path.join(os.getenv("ORIGIN_ROOT"), "origin", "dcc", "gaffer", "startup_gaffer.py")
# exec(open(script_path).read())  # Runs your startup script

import sys
import os


def startup_gaffer():

    print("Running Gaffer startup script...")

    # Ensure ORIGIN_ROOT is set
    origin_root = os.getenv("ORIGIN_ROOT")
    if not origin_root:
        print("ERROR: ORIGIN_ROOT is not set!")
    else:
        print(f"ORIGIN_ROOT is set to: {origin_root}")

    # Determine virtual environment paths
    venv_path = None
    for venv_dir in ["venv", ".venv"]:
        potential_path = os.path.join(origin_root, venv_dir)
        if os.path.exists(potential_path):
            venv_path = potential_path
            break

    if not venv_path:
        print("ERROR: No virtual environment (venv/.venv) found.")
    else:
        print(f"Using virtual environment: {venv_path}")

        # Add virtual environment's site-packages to sys.path
        site_packages = os.path.join(venv_path, "Lib", "site-packages")
        if site_packages not in sys.path:
            sys.path.append(site_packages)
            print(f"Added {site_packages} to sys.path")

    # Try importing pymongo
    try:
        import pymongo
        print(f"Successfully loaded pymongo: {pymongo.__version__}")
    except ModuleNotFoundError:
        print("ERROR: pymongo is not installed in the virtual environment.")


startup_gaffer()
