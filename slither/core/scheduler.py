import logging

from slither.core import graphsearch
from slither.core import storage, node

logger = logging.getLogger(__name__)

# todo: error handling, external processes, logging, job directory


class Status:
    QUEUED = 0
    PENDING = 1
    RUNNING = 2
    FAILED = 3
    COMPLETED = 4
    SCHEDULED = 5


class BaseScheduler(object):
    Type = "base"

    def __init__(self, job):
        self.job = job

    def initialize(self):
        pass

    def shutdown(self):
        pass

    def schedule(self, taskId, nodeInfo):
        raise NotImplementedError()

    def taskStatus(self, taskId):
        raise NotImplementedError()

    def taskResults(self, taskId):
        raise NotImplementedError()


class Job(object):
    def __init__(self, name, application):
        self.name = name
        self.application = application
        self.storage = storage.MemoryStorage()
        self.schedulers = {}
        self.nodes = {}

    def isCompleted(self):
        return self.storage.queueSize() == 0

    def findScheduler(self, schedulerType):
        scheduler = self.schedulers.get(schedulerType)
        if scheduler is not None:
            return scheduler
        scheduler = self.application.registry.schedulerClass(schedulerType, job=self)
        scheduler.initialize()
        self.schedulers[scheduler.Type] = scheduler
        return scheduler

    def schedule(self, graphNode, schedulerType):
        self.nodes[graphNode.id] = graphNode
        scheduler = self.findScheduler(schedulerType)
        taskId = self.storage.generateUniqueId()

        contextData = node.Context.extractContextDataFromNode(graphNode)
        contextData["variables"] = graphNode.graph.variables
        info = {"context": contextData,
                "id": graphNode.id,
                "name": graphNode.name,
                "type": graphNode.Type}

        returnStatus = scheduler.schedule(taskId, info)
        if returnStatus == Status.SCHEDULED:
            print("scheduled: {}".format(graphNode.name))
            self.storage.enqueue(taskId=taskId,
                                 status=Status.QUEUED,
                                 kwargs={"nodeInfo": info,
                                         },

                                 scheduler=scheduler.Type)

    def submit(self, graphNode, schedulerType):
        print("submitting, ", graphNode)
        nodesToSubmit = []
        graphOrder = graphsearch.nodeBreadthFirstSearch(graphNode)

        # grab the leaf nodes
        for n, dependencies in list(graphOrder.items()):
            if not dependencies and n.id in self.nodes:
                del graphOrder[n]
                continue
            for depend in dependencies:
                if depend.id in self.nodes:
                    graphOrder[n].remove(depend)
            if not dependencies:
                nodesToSubmit.append(n)

        if not nodesToSubmit:
            return False
        # schedule the leafNodes
        for n in nodesToSubmit:
            self.schedule(n, schedulerType)
        return True

    def _taskCompleted(self, task):
        # get node dependencies
        self.storage.dequeue(task.id)
        nodeInfo = task.kwargs["nodeInfo"]
        nodeId = nodeInfo["id"]
        node = self.nodes[nodeId]
        results = task.results
        outputInfo = results["outputs"]
        # # in the case where the node is a compound
        # # the outputs could be connected to child nodes
        # # so loop the outputs, find the upstream and add the connected value
        if node.isCompound():
            for output in node.outputs():
                upstream = output.upstream
                if upstream:
                    outputInfo[output.name()] = upstream.value()
        node.copyOutputData(results["outputs"])
        node.setDirty(False)
        
        if node.isCompound():
            self.submit(node, task.scheduler)
        else:
            for depend in node.downStreamNodes():
                if depend.id not in self.nodes:
                    self.schedule(depend, task.scheduler)

    def poll(self):
        completedTasks = []
        for task in self.storage.tasks():
            scheduler = self.findScheduler(task.scheduler)
            status = scheduler.taskStatus(task.id)
            if status == Status.COMPLETED:
                results = scheduler.taskResults(task.id)
                task.status = status
                task.results = results
                completedTasks.append(task)

        for task in completedTasks:
            self._taskCompleted(task)

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        for scheduler in self.schedulers.values():
            scheduler.shutdown()
        self.storage.flushQueue()
        self.storage.shutdown()
