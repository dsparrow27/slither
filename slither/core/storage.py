import dataclasses
import threading
import uuid
from typing import Any


class Storage(object):
    def __init__(self):
        pass

    def start(self):
        pass

    def enqueue(self, taskId, scheduler, status, kwargs):
        pass

    def dequeue(self, taskId):
        pass

    def queueSize(self):
        pass

    def flushQueue(self):
        pass

    def shutdown(self):
        pass

    def tasks(self):
        return []

    def generateUniqueId(self):
        return "0"


class MemoryStorage(Storage):
    def __init__(self):
        super(MemoryStorage, self).__init__()
        self._lock = threading.RLock()
        self.taskQueue = {}  # type: dict[str, Task]

    def generateUniqueId(self):
        return str(uuid.uuid4())

    def enqueue(self, taskId, scheduler, status, kwargs):
        with self._lock:
            self.taskQueue[taskId] = Task(id=taskId,
                                          kwargs=kwargs,
                                          status="queued",
                                          results={},
                                          scheduler=scheduler)
        return True

    def dequeue(self, taskId):
        with self._lock:
            task = self.taskQueue.get(taskId)
            if task is None:
                return
            del self.taskQueue[taskId]
        return task

    def tasks(self):
        return self.taskQueue.values()

    def queueSize(self):
        return len(self.taskQueue.keys())

    def flushQueue(self):
        self.taskQueue = {}


@dataclasses.dataclass
class Task:
    id: int
    status: str
    kwargs: dict
    results: dict
    scheduler: Any = dataclasses.field(repr=False)

    def serialize(self):
        return dataclasses.asdict(self)
