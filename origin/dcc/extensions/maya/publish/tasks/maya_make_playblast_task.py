from origin.dcc.extensions.maya.publish.tasks.abc.batch_task import BatchTask
from origin.dcc.extensions.maya.publish.exporters.maya_make_playblast import MayaMakePlayblast


class MayaMakePlayblastTask(BatchTask):
    def execute(self):
        review_options = self.options.get("review_options", {})
        playblast_obj = MayaMakePlayblast(
            options=self.options,
            frame_range=review_options.get("frame_range"),
            resolution=review_options.get("resolution"),
            resolution_percentage=review_options.get("resolution_percentage"),
            geo_scene_path=review_options.get("geo_scene_path"),
            camera_scene_path=review_options.get("camera_asset_ver_id"),
            template_scene_path=review_options.get("template_asset_ver_id"),
            output_path=review_options.get("output_path")
        )
        playblast_obj.execute()
