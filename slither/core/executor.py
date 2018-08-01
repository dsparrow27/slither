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
            node.progress = 0
            process.start()

    @classmethod
    def stopProcesses(cls, nodes, processes, parentConnections, childConnections):
        if not parentConnections:
            return
        needToTerminate = []
        # determine indices for processes that need to be removed
        for index, childConnection in enumerate(childConnections):
            if childConnection.poll():
                needToTerminate.append(index)

        # loop the indices that need to be removed
        # copy the output data from the process back into the main process output data
        # remove the process/connections/nodes[index] from the storage

        for processIndex in reversed(needToTerminate):
            node = nodes.keys()[processIndex]

            childConnection = childConnections.pop(processIndex)
            node.copyOutputData(childConnection.recv())
            process = processes.pop(processIndex)
            process.join()
            del parentConnections[processIndex]
            del nodes[node]
            node.progress = 100
            for dependent, dependents in nodes.items():
                if node in dependents:
                    nodes[dependent].pop(dependents.index(node))

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

    def execute(self, node):
        if node.isCompound():
            node.mutate()
            nodes = node.topologicalOrder()
        else:
            nodes = service.nodeBreadthFirstSearch(node)

        for n, dependents in nodes.items():
            for d in dependents:
                if len(dependents) == 1 and dependents[0] == n.parent:
                    nodes[n] = list()
                    continue
                self.startProcess(d)
            self.startProcess(n)

    def startProcess(self, node):
        node.progress = 0
        if node.isCompound():
            self.execute(node)
        # compounds can have its own logic once all the children have finished
        if node not in self.visited:
            node.execute()
            node.progress = 100
            self.visited.add(node)
