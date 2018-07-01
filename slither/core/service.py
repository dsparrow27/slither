import logging
from collections import OrderedDict

logger = logging.getLogger("Slither")


def topologicalOrder(nodes):
    unsorted = {}
    for child in nodes:
        dependencies = child.upstreamNodes()  # attribute level dependencies
        unsorted[child] = dependencies

    sortedNodes = OrderedDict()

    while unsorted:
        for node, nodes in unsorted.items():
            for dependent in nodes:
                if dependent in unsorted:
                    break
            else:

                del unsorted[node]
                sortedNodes[node] = nodes

    return sortedNodes


def nodeBreadthFirstSearch(node):
    visited, stack = [], [node]

    while stack:
        current = stack.pop(0)
        upstreams = current.upstreamNodes()
        visited.append(current)
        stack.extend(upstreams)

    return topologicalOrder(visited)
