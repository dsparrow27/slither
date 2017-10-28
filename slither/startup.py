import os
from slither.core import nodeRegistry
from slither.core import typeregistry


def startup():
    NODE_LIB_ENV = "SLITHER_NODE_LIB"
    TYPE_LIB_ENV = "SLITHER_TYPE_LIB"
    # env
    pluginBase = os.path.join(os.path.realpath(os.path.dirname(__file__)), "plugins")
    os.environ[NODE_LIB_ENV] = os.path.join(pluginBase, "nodes")
    os.environ[TYPE_LIB_ENV] = os.path.join(pluginBase, "datatypes")
    typeregistry.DataTypeRegistry()
    nodeRegistry.NodeRegistry()
