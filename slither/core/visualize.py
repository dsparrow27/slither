"""Modules which contains utility functions for creating visual representation
of a graph using pydot.

requirements:
pydot
graphviz/bin on PATH
"""
import pydot


def buildGraph(node, filePath):
    order = node.topologicalOrder()
    graph = pydot.Dot(graph_name="parentGraph", rankdir='LR')
    rootNode = pydot.Subgraph(node.name)
    graph.add_subgraph(rootNode)

    for n, dependents in order.items():
        downstream = pydot.Node(name=n.name, shape="box")
        rootNode.add_node(downstream)
        for depend in dependents:
            pyn = pydot.Node(depend.name, shape="box")
            rootNode.add_edge(pydot.Edge(pyn, downstream))
    graph.write_png(filePath)
