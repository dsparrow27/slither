import multiprocessing

from slither import api


class Parallel(api.BaseScheduler):
    """Background scheduler using subprocess per node. The process is still blocked at this time
    but all node computations are done in parallel.
    """

    Type = "parallel"

    def __init__(self, job):
        super(Parallel, self).__init__(job)
        self._tasks = {}  # nodeId: {"parentConnection": "", "childConnection": "" }

    def shutdown(self):
        self._tasks = {}

    def schedule(self, taskId, nodeInfo):
        parent, child = multiprocessing.Pipe()
        process = multiprocessing.Process(target=executeNode, args=(nodeInfo, parent))
        self._tasks[taskId] = {"parentConnection": parent,
                               "childConnection": child,
                               "process": process,
                               "status": api.Status.RUNNING}
        process.start()
        return api.Status.SCHEDULED

    def taskStatus(self, taskId):

        task = self._tasks.get(taskId, {})
        connection = task["childConnection"]

        if not connection.poll():
            task["status"] = api.Status.RUNNING
            return api.Status.RUNNING
        task["process"].join()
        task["status"] = api.Status.COMPLETED
        return api.Status.COMPLETED

    def taskResults(self, taskId):
        task = self._tasks.get(taskId, {})

        connection = task["childConnection"]
        if not connection.poll():
            return {}

        data = connection.recv()
        task["process"].join()
        return data


def executeNode(nodeInfo, connection):
    nodeApp = api.Application()
    graph = nodeApp.createGraph("ExecutionGraph-{}".format(nodeInfo["name"]))
    graph.variables = nodeInfo["context"]["variables"]
    newNode = graph.createNode(nodeInfo["name"], nodeInfo["type"])
    context = api.Context.fromExtractData(nodeInfo["context"])
    newNode.proxyCls.compute(context)
    connection.send(context.serialize())
