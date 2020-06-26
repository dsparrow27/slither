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
                if dependent in unsorted:
                    break
            else:
                del resolve[node]
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
