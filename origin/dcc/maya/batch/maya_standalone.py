import argparse
import json
import maya.standalone
import maya.cmds as cmds
from origin.dcc.env_setup import env_setup
from origin.dcc.maya.batch.tasks.batch_task_factory import TASKS


def load_additional_plugins():
    plugins = ["AbcImport", "AbcExport", "objExport"]
    for plugin in plugins:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            print(f"Loading plugin: {plugin}")
            cmds.loadPlugin(plugin)
        else:
            print(f"'{plugin}' is already loaded.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a Maya Export Task in batch mode.")
    parser.add_argument("--task", type=str, required=True, help="The task to execute (e.g., 'playblast', 'render', 'geo_export').")
    parser.add_argument("--options", type=str, required=True, help="Serialized JSON string of options.")
    return parser.parse_args()


def main():
    maya.standalone.initialize(name='python')

    try:
        env_setup()
        load_additional_plugins()
        args = parse_arguments()

        # Parse the options JSON string into a dictionary
        options = json.loads(args.options)

        task_class = TASKS.get(args.task)
        task = task_class(options)
        task.execute()

    finally:
        maya.standalone.uninitialize()


if __name__ == "__main__":
    main()
