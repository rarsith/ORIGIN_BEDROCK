import os
from envars.envars import Envars

def get_path(filename):
    path_loc = os.path.realpath(os.path.join(__file__,"../..","o_database","schemas", "templates", filename))
    return path_loc

if __name__ == '__main__':
    xx = get_path("new_tasks_default_schemas.json")
    print(xx)