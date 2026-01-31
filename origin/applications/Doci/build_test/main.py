from origin.applications.Doci.build_test.publish import Publish
from origin.applications.Doci.build_test.logger import PublishLogger
from origin.applications.Doci.build_test.tasks.geometry_export import GeometryExport
from origin.applications.Doci.build_test.tasks.playblast_export import PlayblastExport
from origin.applications.Doci.build_test.tasks.mov_export import MovExport

context = {
    "mayapy": r"D:/Program Files/Autodesk/Maya2024/bin/mayapy.exe",
    "geo_script": "geo_export.py",
    "playblast_script": "playblast.py"
}

logger = PublishLogger("publish_log.json")
Publish = Publish(context, logger)

geo_export = Publish.addTask(
    GeometryExport(scene="asset.ma", out_dir="X:/publish/geo")
)

playblast = Publish.addTask(
    PlayblastExport(playblast_scene="turntable.ma", dependent=geo_export)
)

movie_make = Publish.addTask(
    MovExport(dependent=playblast)
)

Publish.run()
