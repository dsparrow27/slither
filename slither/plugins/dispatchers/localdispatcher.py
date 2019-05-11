from slither.core import service
from slither.core.node import Context
from slither.core import dispatcher


class StandardExecutor(dispatcher.BaseDispatcher):
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
        ctx["variables"] = self.graph.variables
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
