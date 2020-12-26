import threading
import uuid


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
        # data = {"taskId": "",
        #         "kwargs": {},
        #         "status": "",
        #         "results": {},
        #         "scheduler": ""}
        self.taskQueue = {}

    def generateUniqueId(self):
        return str(uuid.uuid4())

    def enqueue(self, taskId, scheduler, status, kwargs):
        with self._lock:
            self.taskQueue[taskId] = {"taskId": taskId,
                                      "kwargs": kwargs,
                                      "status": "queued",
                                      "results": {},
                                      "scheduler": scheduler}
        return True

    def dequeue(self, taskId):
        with self._lock:
            task = self.taskQueue.get(taskId)
            if task is None:
                return
            del self.taskQueue[taskId]
        return task

    def tasks(self):
        return map(Task, self.taskQueue.values())

    def queueSize(self):
        return len(self.taskQueue.keys())

    def flushQueue(self):
        self.taskQueue = {}


class Task(object):
    def __init__(self, data):
        self.id = data["taskId"]
        self.status = data["status"]
        self.kwargs = data["kwargs"]
        self.results = data["results"]
        self.scheduler = data["scheduler"]

    def __hash__(self):
        return hash(id(self))

    def serialize(self):
        return {
            "taskId": self.id,
            "status": self.status,
            "kwargs": self.kwargs,
            "results": self.results,
            "scheduler": self.scheduler.id
        }
