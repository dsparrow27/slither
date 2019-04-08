import logging
import os

from slither.core import application as _application
from slither.core.attribute import (AttributeDefinition, Attribute, CompoundAttribute, ArrayAttribute)
from slither.core.node import BaseNode, Compound
from slither.core.executor import (StandardExecutor, Parallel)
from slither.core.types import DataType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Slither")
logger.addHandler(logging.StreamHandler())

currentInstance = None
instances = []


def standalone():
    print __file__
    pluginDir = r"D:\dave\code\python\tools\personal\slither\slither\plugins"
    nodeDir = os.path.join(pluginDir, "nodes")
    typeDir = os.path.join(pluginDir, "datatypes")
    os.environ["SLITHER_NODE_LIB"] = os.pathsep.join([os.path.join(nodeDir, "generic")])
    os.environ["SLITHER_TYPE_LIB"] = os.pathsep.join([os.path.join(typeDir, "generic")])


def newInstance(current=True):
    global currentInstance, instances

    app = _application.Application()
    instances.append(app)
    if current:
        currentInstance = app
    return app


def clearInstances():
    global currentInstance, instances
    for instance in instances:
        instance.shutdown()
    instances = []
    currentInstance = None


standalone()
currentInstance = newInstance()
