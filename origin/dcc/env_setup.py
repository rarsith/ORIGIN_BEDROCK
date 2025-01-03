import os
import sys
from pathlib import Path


def env_setup():
    pass
    origin_root = os.getenv("ORIGIN_ROOT")

    origin_pipe_root = Path(origin_root)
    origin_site_packages = Path(".venv") / "Lib" / "site-packages"
    pymongo_parent_dir = origin_pipe_root / origin_site_packages

    origin_user_setup = Path("origin") / "dcc" / "maya"
    maya_origin_user_setup = origin_pipe_root / origin_user_setup

    if str(pymongo_parent_dir) not in sys.path:
        sys.path.append(str(pymongo_parent_dir))

    if str(maya_origin_user_setup) not in sys.path:
        sys.path.append(str(maya_origin_user_setup))

    existing_pythonpath = os.getenv("PYTHONPATH")
    if existing_pythonpath:
        os.environ["PYTHONPATH"] = f"{pymongo_parent_dir};{existing_pythonpath}"
    else:
        os.environ["PYTHONPATH"] = str(pymongo_parent_dir)

    try:
        import pymongo
        print("----> Imported PYMONGO")
        import pydantic
        print("----> Imported PYDANTIC")
        import logging
        print("----> Imported LOGGING")

        logging.getLogger("pymongo").setLevel(logging.ERROR)

        print("----> ORIGIN site-packages added to current session!")

    except ImportError as e:
        print("Error importing pymongo:", e)
