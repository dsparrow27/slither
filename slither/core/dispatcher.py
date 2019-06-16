import logging

logger = logging.getLogger(__name__)


class BaseDispatcher(object):
    Type = "base"

    def __init__(self, graph):
        self.graph = graph
        self.logger = logger

    def execute(self, node):
        raise NotImplementedError("Execute method isn't implemented")
    @classmethod
    def onNodeCompleted(cls, node, context):
        outputInfo = {k: Type.value() for k, Type in context["outputs"].items()}
        # in the case where the node is a compound
        # the outputs could be connected to child nodes
        # so loop the outputs, find the upstream and add the connected value
        if node.isCompound:
            for output in node.outputs():
                upstream = output.upstream

                if upstream:
                    outputInfo[output.name()] = upstream.value()
        node.copyOutputData(outputInfo)
