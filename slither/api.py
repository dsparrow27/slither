import os

from zoo.libs.utils import zlogging
from zoo.libs.utils import env

from slither.core import application as _application
from slither.core.attribute import (AttributeDefinition, Attribute, CompoundAttribute, ArrayAttribute)
from slither.core.node import BaseNode, Compound, Pin, Comment, ComputeNode
from slither.core.executor import (StandardExecutor, Parallel)
from slither.core import types
from slither.core.types import DataType

logger = zlogging.getLogger(__name__)

NODE_LIB_ENV = "SLITHER_NODE_LIB"
TYPE_LIB_ENV = "SLITHER_TYPE_LIB"

currentInstance = None
instances = []


def mayaEnv():
    from pw.libs.shotgun import utils
    engine = utils.currentEngine()
    root = os.path.join(engine.apps["tk-zeus"].disk_location, "python")
    pluginBase = os.path.join(root, "pw/zeus", "plugins")
    nodeLib = os.pathsep.join([os.path.join(pluginBase, "nodes/generic"), os.path.join(pluginBase, "nodes/maya"),
                               os.path.join(pluginBase, "nodes/shotgun")])
    os.environ["SLITHER_NODE_LIB"] = nodeLib
    os.environ["SLITHER_TYPE_LIB"] = os.pathsep.join([os.path.join(pluginBase, "datatypes/generic"),
                                                   os.path.join(pluginBase, "datatypes/maya"),
                                                   os.path.join(pluginBase, "datatypes/shotgun")])


def newInstance(current=True):
    global currentInstance, instances

    app = _application.Application()
    app.initialize()
    instances.append(app)
    if current:
        currentInstance = app
    return app


def clear():
    global currentInstance, instances
    for i in instances:
        i.shutdown()
    instances = []
    currentInstance = None
# temp
if env.isInMaya():
    mayaEnv()

currentInstance = newInstance()
