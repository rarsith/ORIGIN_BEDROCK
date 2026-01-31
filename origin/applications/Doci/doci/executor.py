from origin.applications.Doci.handlers.maya_geometry import MayaGeometryPublish

HANDLERS = {
    MayaGeometryPublish.JOB_TYPE: MayaGeometryPublish()
}

class Executor:
    def execute(self, job):
        handler = HANDLERS.get(job.job_type)
        if not handler:
            raise RuntimeError(f"No handler for {job.job_type}")

        handler.run(job)