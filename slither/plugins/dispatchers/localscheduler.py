from slither import api


class InProcessScheduler(api.BaseScheduler):
    """Serial graph scheduler, in this case all processing will block the
    current process.
    """
    Type = "inProcess"

    def __init__(self, *args, **kwargs):
        super(InProcessScheduler, self).__init__(*args, **kwargs)
        self._tasks = {}

    def schedule(self, taskId, nodeInfo):
        context = api.Context.fromExtractData(nodeInfo["context"])
        nodeClass, _ = self.job.application.registry.proxyNodeClass(nodeInfo["type"])
        nodeClass.compute(context=context)
        self._tasks[taskId] = {"status": api.Status.COMPLETED,
                               "node": nodeClass,
                               "context": context}
        return api.Status.SCHEDULED

    def taskStatus(self, taskId):
        return self._tasks.get(taskId, {})["status"]

    def taskResults(self, taskId):
        return self._tasks.get(taskId)["context"].serialize()
