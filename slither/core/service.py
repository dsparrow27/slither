import logging
from collections import OrderedDict
from slither.core import attribute

logger = logging.getLogger("Slither")

def topologicalOrder(nodes):
    unsorted = {}
    for child in nodes:
        dependencies = child.upstreamNodes() # attribute level dependencies
        dependencies.extend(child.dependencies) # add the node level dependencies
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


def siblingNodes(node):
    """Finds and returns all the siblings nodes under the node parent

    :param node:
    :type node: BaseNode instance
    :return:
    :rtype: list(Basenode instance)
    """
    nodes = []
    if node.parent:
        for i in node.parent:
            if i != node:
                nodes.append(i)
    return nodes


def upstreamNodes(node):
    nodes = []
    for input_ in node.iterInputs():
        if input_.hasUpstream():
            nodes.append(input_.upstream.parent)
    return nodes


def downStreamNodes(node):
    nodes = []
    if node.parent:
        children = node.parent.children
        for i in children:
            if node in i.upstreamNodes():
                nodes.append(i)
    return nodes


def serializeCompound(compound, recursive=True):
    data = {}
    for child in compound.children:
        if recursive and child.isCompound():
            data = serializeCompound(child, recursive)
            data[child.fullName()] = data
            continue
        data[child.fullName()] = child.serialize()
    return data


def createAttribute(nodeInstance, attributeDefinition):
    if nodeInstance.hasAttribute(attributeDefinition.name):
        logger.error("Can't create attribute: {} because it already exists".format(attributeDefinition.name))
        raise ValueError("Name -> {} already exists".format(attributeDefinition.name))
    logger.debug("Creating Attribute: {} on node: {}".format(attributeDefinition.name,
                                                             nodeInstance.name))
    if attributeDefinition.isArray:
        newAttribute = attribute.ArrayAttribute(attributeDefinition, node=nodeInstance)
    elif attributeDefinition.isCompound:
        newAttribute = attribute.CompoundAttribute(attributeDefinition, node=nodeInstance)
    else:
        newAttribute = attribute.Attribute(attributeDefinition, node=nodeInstance)
    return newAttribute


def copyOutputData(node, outputs):
    for name, value in iter(outputs.items()):
        attr = node.attribute(name)
        if attr is not None:
            attr.setValue(value)
