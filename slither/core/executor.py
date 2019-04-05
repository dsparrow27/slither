import multiprocessing

from slither.core import service


class Executor(object):
    Type = "base"


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
                node.setDirty(False, False)
                node.progress = 100
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
        node.execute()
        outputs = node.outputs()
        data = {}
        for output in outputs:
            data[output.name()] = output.value()
        parentConnection.send(data)


class StandardExecutor(Executor):
    Type = "Serial"

    def __init__(self):
        self.visited = set()

    def _dependents(self, node):
        if node.isCompound():
            node.mutate()
            return node.topologicalOrder()
        return service.nodeBreadthFirstSearch(node)

    def startProcess(self, node):
        nodes = self._dependents(node)
        for n, dependents in nodes.items():
            for d in dependents:
                if d.progress == 100:
                    continue
                if len(dependents) == 1 and dependents[0] == n.parent:
                    nodes[n] = list()
                    continue
                self.execute(d)
            if n.progress == 100:
                self.execute(n)

    def execute(self, node):
        node.progress = 0
        try:
            if node.isCompound():
                self.startProcess(node)
                node.execute()
            else:
                node.execute()
            node.setDirty(False, False)
        finally:
            node.progress = 100
        return True
