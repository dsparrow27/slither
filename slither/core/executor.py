import multiprocessing
import pprint

from slither.core import service
from slither.core.node import Context


class Executor(object):
    Type = "base"

    def __init__(self, application):
        self.application = application


class Parallel(Executor):
    Type = "Parallel"

    @classmethod
    def execute(cls, node):
        """Executes a given node in parellel if the node is a compound then the children will be executed
        :param node: Node instance, either a compound or a subclass of node
        :return: bool, True when finished executing nodes
        """
        if node.isCompound():
            node.mutate()
            nodes = node.topologicalOrder()
        else:
            nodes = service.nodeBreadthFirstSearch(node)
        processes = []
        parentConnections = []
        childConnections = []
        while nodes:
            cls.stopProcesses(nodes, processes, parentConnections, childConnections)
            cls.startProcesses(nodes, processes, parentConnections, childConnections)
        return True

    @classmethod
    def startProcesses(cls, nodes, processes, parentConnections, childConnections):
        """
        :param nodes: list(node), a list of nodes to execute
        :param processes: list(multiprocessing.Process), a list of processing class
        :param parentConnections: list(multiprocessing.Connection), a list of parent connections which will store the
        processed nodes output values as a dict
        :param childConnections: list(multiprocessing.Connection)
        """
        for node, dependents in nodes.items():
            if dependents:
                if len(dependents) == 1 and dependents[0] == node.parent:
                    nodes[node] = list()
                else:
                    continue
            parentConnection, childConnection = multiprocessing.Pipe()
            parentConnections.append(parentConnection)
            childConnections.append(childConnection)
            process = multiprocessing.Process(target=cls.startProcess(node, parentConnection))
            processes.append(process)

            process.start()

    @classmethod
    def stopProcesses(cls, nodes, processes, parentConnections, childConnections):
        if not parentConnections:
            return
        needToTerminate = []
        # determine indices for processes that need to be removed
        for index, childConnection in enumerate(childConnections):
            if childConnection.poll():
                recvData = childConnection.recv()
                node = nodes.keys()[index]
                # copy the output data from the process back into the main process output data
                node.copyOutputData(recvData)
                del nodes[node]
                for dependent, dependents in nodes.items():
                    if node in dependents:
                        nodes[dependent].pop(dependents.index(node))
                needToTerminate.append(index)
        # loop the indices that need to be removed

        # remove the process/connections/nodes[index] from the storage
        for processIndex in reversed(needToTerminate):
            childConnections.pop(processIndex)
            process = processes.pop(processIndex)
            process.join()
            del parentConnections[processIndex]

    @classmethod
    def startProcess(cls, node, parentConnection):
        if node.isCompound():
            cls.execute(node)
        node.process()
        outputs = node.outputs()
        data = {}
        for output in outputs:
            data[output.name()] = output.value()
        parentConnection.send(data)


class StandardExecutor(Executor):
    Type = "Serial"

    def _dependents(self, node):
        if node.isCompound():
            node.mutate()
            return node.topologicalOrder()
        return service.nodeBreadthFirstSearch(node)

    def startProcess(self, node):
        nodes = self._dependents(node)
        visited = set()
        for n, dependents in nodes.items():

            for d in dependents:
                if d in visited:
                    dependents.remove(d)
                    continue
                if len(dependents) == 1 and dependents[0] == n.parent:
                    nodes[n] = list()
                    continue
                self.processNode(d)
                visited.add(d)
            self.processNode(n)
            visited.add(n)

    def processNode(self, node):
        if node.isCompound():
            self.startProcess(node)
        ctx = Context.fromNode(node)
        ctx["variables"] = self.application.variables
        node.process(ctx)
        outputInfo = {k: Type.value() for k, Type in ctx["outputs"].items()}
        # in the case where the node is a compound
        # the outputs could be connected to child nodes
        # so loop the outputs, find the upstream and add the connected value
        if node.isCompound:
            for output in node.outputs():
                upstream = output.upstream
                if upstream:
                    outputInfo[output.name()] = upstream.value()
        node.copyOutputData(outputInfo)

    def execute(self, node):
        self.processNode(node)
        return True
