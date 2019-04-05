import os
from zoo.libs.utils import filesystem
from slither.core import executor, node, types
from zoo.libs.plugin import pluginmanager

import logging

logger = logging.getLogger(__name__)


class Application(object):
    PARALLELEXECUTOR = 0
    STANDARDEXECUTOR = 1
    NODE_LIB_ENV = "SLITHER_NODE_LIB"
    TYPE_LIB_ENV = "SLITHER_TYPE_LIB"

    def __init__(self):
        self.nodeRegistry = pluginmanager.PluginManager(node.BaseNode, variableName="type")
        self.typeRegistry = pluginmanager.PluginManager(types.DataType, variableName="Type")
        self.nodeRegistry.registerPaths(os.environ[Application.TYPE_LIB_ENV].split(os.pathsep))
        self.typeRegistry.registerPaths(os.environ[Application.NODE_LIB_ENV].split(os.pathsep))
        # add the compound base node
        self.nodeRegistry.registerPlugin(node.Compound)

        self._root = None
        self.globals = {}

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def shutdown(self):
        pass

    def dataType(self, typeName):
        return self.typeRegistry.loadPlugin(typeName)

    @property
    def root(self):
        if self._root is not None:
            return self._root
        self._root = self.nodeRegistry.loadPlugin("Compound", name="Root System", application=self)
        # mark the root as internal and locked so it can't be deleted.
        self._root.isLocked = True
        self._root.isInternal = True
        return self._root

    def save(self, filePath, node=None):
        node = node or self.root
        data = node.serialize()
        filesystem.saveJson(data, filePath)
        return os.path.exists(filePath)

    def execute(self, node, executorType):
        if executorType == Application.PARALLELEXECUTOR:
            logger.debug("Starting execution")
            exe = executor.Parallel()
            exe.execute(node)
            logger.debug("finished")
            return True
        elif executorType == Application.STANDARDEXECUTOR:
            exe = executor.StandardExecutor()
            exe.execute(node)
            return True
        return False
