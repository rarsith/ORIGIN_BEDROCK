import Gaffer
import GafferScene
import GafferDispatch

# Load the existing Gaffer template
script = Gaffer.ScriptNode()
script["fileName"].setValue("D:/__SANDBOX/__test_scenes/AlienHead/DATA_PACKAGE/gaffer_templates/lookdev/templat_v001.gfr")
script.load()

# Inject the Alembic cache
alembic_cache = script['Asset_Load']
alembic_cache["fileName"].setValue("D:/__SANDBOX/__test_scenes/AlienHead/DATA_PACKAGE/geo/alien_geometry_v002.abc")

referenceLookNode = Gaffer.Reference()
script.addChild( referenceLookNode )
referenceLookNode.load( "D:/__SANDBOX/__test_scenes/AlienHead/DATA_PACKAGE/gaffer_templates/lookdev/lights.gfr" )

print("END")
#
# # Connect the Alembic cache to the lookdev box or other nodes
# # Assuming you have a lookdev box node in the template
# lookdev_box = script["Look_Dev"]
# lookdev_box["in"].setInput(alembic_cache["out"])
#
# # Configure the render node
# render = GafferScene.InteractiveRender()
# render["in"].setInput(lookdev_box["out"])
# render["state"].setValue(GafferScene.InteractiveRender.State.Running)
#
# # Add the render node to the script
# script["render"] = render
#
# # Save the modified script if needed
# script["fileName"].setValue("/path/to/your/modified_template.gfr")
# script.save()
#
# # Execute the render in batch mode
# dispatcher = GafferDispatch.LocalDispatcher()
# dispatcher["jobsDirectory"].setValue("/path/to/jobs")
# dispatcher["framesMode"].setValue(GafferDispatch.Dispatcher.FramesMode.FullRange)
# dispatcher["frameRange"].setValue("1-30")  # Specify your frame range here
# dispatcher.dispatch([render])