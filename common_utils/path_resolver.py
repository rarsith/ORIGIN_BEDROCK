import os
from envars.envars import Envars

def get_path(filename):
    path_loc = os.path.realpath(os.path.join(__file__,"../..","database","defaults", filename))
    return path_loc

if __name__ == '__main__':
    get_path("show_default_schemas.json")