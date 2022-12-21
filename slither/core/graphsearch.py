import logging
from collections import OrderedDict
from zoo.core.util import zlogging

logger = zlogging.getLogger(__name__)

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


def nodeBreadthFirstSearch(node, dirty=False):
    """

    :param node:
    :type node: :class:`slither.core.node.ComputeNode`
    :param dirty: If True then dirty nodes will also be included in the returned search
    :type dirty: bool
    :return:
    :rtype: OrderedDict[:class:`slither.core.node.ComputeNode`: list[:class:`slither.core.node.ComputeNode`]]
    """
    ordered = OrderedDict()
    stack = []
    if node.isCompound():
        for output in node.outputs():
            for upstream in output.upstream():
                n = upstream.node
                if n not in stack or n != node and (not dirty and n.dirty()):
                    stack.append(n)
    else:
        stack.append(node)
    while stack:
        m = stack.pop()
        if not dirty:
            depends = [i for i in m.upstreamNodes() if i not in stack and i.dirty()]
        else:
            depends = [i for i in m.upstreamNodes() if i not in stack]
        stack.extend(depends)
        if m in ordered:
            continue
        ordered[m] = depends
    return OrderedDict(reversed(list(ordered.items())))
