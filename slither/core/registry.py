import os
import logging
from slither.core import types
from zoo.libs.plugin import pluginmanager
from slither.core import node
from slither.core import compound
from slither.core import classtypes

logger = logging.getLogger(__name__)


class NodeRegistry(pluginmanager.PluginManager):
    __metaclass__ = classtypes.Singleton
    NODE_LIB_ENV = "SLITHER_NODE_LIB"

    def __init__(self):
        super(NodeRegistry, self).__init__(interface=node.BaseNode)
        self.registerPaths(os.environ[NodeRegistry.NODE_LIB_ENV].split(os.pathsep))
        # add the compound base node
        self.registerPlugin(compound.Compound)


class DataTypeRegistry(pluginmanager.PluginManager):
    __metaclass__ = classtypes.Singleton
    TYPE_LIB_ENV = "SLITHER_TYPE_LIB"

    def __init__(self):
        super(DataTypeRegistry, self).__init__(types.DataType, variableName="Type")
        self.registerPaths(os.environ[DataTypeRegistry.TYPE_LIB_ENV].split(os.pathsep))
        self.registerPlugin(types.DataType)
