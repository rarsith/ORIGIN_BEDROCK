from origin.applications.Doci.doci.job import Job
from origin.applications.Doci.doci.executor import Executor


def run_sample():
    job = Job(
        job_type="maya_geometry_publish",
        payload={
            "scene": "X:/projects/Small_Rock/assets/characters/hulk/modeling/publishes/data/geometry__hulk__hulk_MAIN/characters__hulk__hulk_MAIN__v0002/origin_scene/characters__hulk__hulk_MAIN__v0002.mb",
            "output_dir": "X:/projects/Small_Rock/assets/characters/hulk/modeling/publishes/data/geometry__hulk__hulk_MAIN/characters__hulk__hulk_MAIN__v0002"
        }
    )

    Executor().execute(job)

if __name__ == "__main__":
    run_sample()