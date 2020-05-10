import multiprocessing
import timeit

from slither.core import service
from slither.core import dispatcher
from slither.core.node import Context


class Parallel(dispatcher.BaseDispatcher):
    """Background dispatcher using subprocess per node. The process is still blocked at this time
    but all node computations are done in parallel.
    """
    Type = "Parallel"

    def execute(self, node):
        """Executes a given node in parallel if the node is a compound then the children will be executed

        :param node: Node instance, either a compound or a subclass of node
        :return: bool, True when finished executing nodes
        """
        start = timeit.default_timer()
        try:
            self._execute(node)
        finally:
            end = timeit.default_timer()
            totalExecutionTime = end - start

            self.logger.debug("Total executing time: {}".format(totalExecutionTime))

    @classmethod
    def _execute(cls, node):

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
                cls.onNodeCompleted(node, recvData)
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
            cls._execute(node)
        ctx = Context.fromNode(node)
        node.process(ctx)
        parentConnection.send(ctx)
