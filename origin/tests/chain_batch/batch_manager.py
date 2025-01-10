import os
import queue
import subprocess
import threading


class BatchJobManager:
    def __init__(self):
        self.jobs = []
        self.job_queue = queue.Queue()

    def add_job(self, name, script, dependencies=None):
        """Add a job to the manager."""
        job = {
            "name": name,
            "script": script,
            "dependencies": dependencies or [],
            "status": "pending",
            "output": None,  # Store job output here
        }
        self.jobs.append(job)
        return job

    def execute(self):
        """Execute jobs respecting dependencies."""
        threads = []

        # Add jobs to the queue
        for job in self.jobs:
            self.job_queue.put(job)

        # Start threads for job execution
        for _ in range(len(self.jobs)):
            thread = threading.Thread(target=self._process_job)
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def _process_job(self):
        while not self.job_queue.empty():
            job = self.job_queue.get()

            # Check dependencies
            if all(dep["status"] == "completed" for dep in job["dependencies"]):
                self._run_job(job)
                job["status"] = "completed"
            else:
                self.job_queue.put(job)  # Re-queue for later

    def _run_job(self, job):
        """Execute the script of the job and capture its output."""
        print(f"Running job: {job['name']}")
        try:
            # Pass outputs of dependencies to the job as environment variables
            env = os.environ.copy()
            for dep in job["dependencies"]:
                env[f"{dep['name']}_OUTPUT"] = dep["output"] or ""

            # Execute the script
            result = subprocess.run(["mayapy", job["script"]], capture_output=True, text=True, env=env, check=True)

            # Store the output of the job
            job["output"] = result.stdout.strip()
            print(f"Job {job['name']} completed with output: {job['output']}")
        except subprocess.CalledProcessError as e:
            print(f"Job {job['name']} failed: {e}")
            job["status"] = "failed"
