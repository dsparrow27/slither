import pydot


def exportGraph(root, filePath):
    """Exports the given root graph
    :param root:
    :type root: :class:`Node`
    :param filePath: the output file path.png
    """
    graph = pydot.Dot(root.name)

    def _recusiveDraw(compound):
        parent = pydot.Subgraph(compound.name)
        graph.add_node(parent)
        for subChild in parent.children():
            child = pydot.Node(subChild.name, shape="box")
            for attr in subChild.attributes():
                connection = attr.upstream
                if connection is not None:
                    parent.add_edge(pydot.Edge(connection.node.name, child.name))
            if child.isCompound:
                _recusiveDraw(child)
    _recusiveDraw(root)
    graph.write_png(filePath)