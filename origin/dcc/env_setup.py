import os
import sys
from pathlib import Path


def env_setup():

    origin_root = os.getenv("ORIGIN_ROOT")

    origin_pipe_root = Path(origin_root)
    origin_site_packages = Path("venv") / "Lib" / "site-packages"
    origin_pyhon_dev = origin_pipe_root / origin_site_packages

    origin_user_setup = Path("origin") / "dcc" / "extensions" / "maya"
    maya_origin_user_setup = origin_pipe_root / origin_user_setup

    print(maya_origin_user_setup)

    if str(origin_pyhon_dev) not in sys.path:
        sys.path.append(str(origin_pyhon_dev))

    if str(maya_origin_user_setup) not in sys.path:
        sys.path.append(str(maya_origin_user_setup))

    existing_pythonpath = os.getenv("PYTHONPATH")
    if existing_pythonpath:
        os.environ["PYTHONPATH"] = f"{origin_pyhon_dev};{existing_pythonpath}"
    else:
        os.environ["PYTHONPATH"] = str(origin_pyhon_dev)

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


if __name__ == "__main__":
    # xx = os.path.join(os.getenv('ORIGIN_ROOT'), 'origin/dcc/extensions/maya/bin/startup/')
    # print(xx)
    env_setup()
