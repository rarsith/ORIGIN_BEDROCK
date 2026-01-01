import time
from watchdog.observers import Observer
from watcher import OriginWatcher
from dispatcher import Dispatcher
from executor_local import LocalExecutor

executor = LocalExecutor(max_workers=8)
dispatcher = Dispatcher(executor)

observer = Observer()
observer.schedule(
    OriginWatcher(dispatcher),
    path="../jobs/incoming",
    recursive=False
)

observer.start()
print("DOCI is alive.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()