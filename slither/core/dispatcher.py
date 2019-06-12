class BaseDispatcher(object):
    Type = "base"

    def __init__(self, graph):
        self.graph = graph

    def execute(self, node):
        raise NotImplementedError("Execute method isn't implemented")
