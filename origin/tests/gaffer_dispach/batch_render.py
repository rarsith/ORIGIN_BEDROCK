import Gaffer
import GafferDispatch
import GafferScene

# Load the Gaffer script
script = Gaffer.ScriptNode()
script["fileName"].setValue("D:/__SANDBOX/__test_scenes/AlienHead/DATA_PACKAGE/alien__lookdev_v003.gfr")
script.load()

# List available nodes for debugging
print("Available nodes:")
for node_name in script.keys():
    print(f"Node: {node_name}, Type: {type(script[node_name])}")

# Get the render node
render_node = script["Render"]  # Replace with the correct node name
print(render_node.keys())  # Debug: list render node plugs

# Configure the dispatcher
dispatcher = GafferDispatch.LocalDispatcher()
dispatcher["jobsDirectory"].setValue("D:/__SANDBOX/__test_scenes/AlienHead/DATA_PACKAGE")
dispatcher["executeInBackground"].setValue(True)

# Dispatch the render task
dispatcher["nodes"] = Gaffer.StandardSet([render_node])
dispatcher.dispatch()
