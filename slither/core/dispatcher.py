import logging
import os
import tempfile

logger = logging.getLogger(__name__)


class BaseDispatcher(object):
    Type = "base"

    def __init__(self, graph):
        self.graph = graph
        self.logger = logger
        self._tempDir = ""

    def tempDir(self):
        return self._tempDir

    def createTempDirectory(self):
        customTempDir = os.environ.get("SLITHER_DISPATCH_TEMP")
        if not os.path.exists(customTempDir):
            self._tempDir = tempfile.mkdtemp()
        self._tempDir = customTempDir

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
