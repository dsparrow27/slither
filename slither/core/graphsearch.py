import logging
from collections import OrderedDict

logger = logging.getLogger("Slither")


def topologicalOrder(nodes):
    sortedNodes = OrderedDict()
    unsorted = {}
    for child in nodes:
        dependencies = child.upstreamNodes()  # attribute level dependencies
        unsorted[child] = dependencies
    resolve = dict(unsorted)

    while resolve:
        for node, nodes in unsorted.items():
            for dependent in nodes:
                if dependent in sortedNodes:
                    break
            else:
                del resolve[node]
                sortedNodes[node] = nodes

    return sortedNodes


def nodeBreadthFirstSearch(node):
    stack = []
    if node.isCompound():
        for output in node.outputs():
            upstream = output.upstream
            if upstream:
                n = upstream.node
                if n not in stack:
                    stack.append(n)
    else:
        stack.append(node)
    ordered = OrderedDict()
    while stack:
        m = stack.pop()
        depends = m.upstreamNodes()
        stack.extend(depends)
        ordered[m] = depends
    return OrderedDict(reversed(list(ordered.items())))



