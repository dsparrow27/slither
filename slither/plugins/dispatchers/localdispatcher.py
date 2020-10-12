import timeit

from slither import api


class StandardExecutor(api.BaseDispatcher):
    """Serial graph dispatcher, in this case all processing will block the
    current process.
    """
    Type = "serial"

    def _dependents(self, node):
        if node.isCompound():
            node.mutate()
            return node.topologicalOrder()
        return api.nodeBreadthFirstSearch(node)

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
        ctx = api.Context.fromNode(node)
        ctx["variables"] = self.graph.variables
        node.process(ctx)
        self.onNodeCompleted(node, ctx)

    def execute(self, node):
        start = timeit.default_timer()
        self.processNode(node)
        self.logger.debug("Total executing time: {}".format(timeit.default_timer()-start))
        return True
