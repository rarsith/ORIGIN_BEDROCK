from origin.dcc.maya.batch.tasks.maya_geometry_exporter_task import MayaGeometryExporterTask
from origin.dcc.maya.batch.tasks.maya_make_playblast_task import MayaMakePlayblastTask
from origin.dcc.maya.batch.tasks.maya_publish_task import MayaPublishTask


TASKS = {
    "playblast": MayaMakePlayblastTask,
    "publish": MayaPublishTask,
    "anim_rig": "",
    "geometry": MayaGeometryExporterTask,
    "camera": "",
    "template": "",
    "point_cache": "",
    # Add other tasks here
}
