import logging


from slither.core import application as _application
from slither.core.attribute import (AttributeDefinition, Attribute, CompoundAttribute, ArrayAttribute)
from slither.core.node import BaseNode, Compound
from slither.core.executor import (StandardExecutor, Parallel)
from slither.core.types import DataType


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Slither")
logger.addHandler(logging.NullHandler())

currentInstance = None
instances = []


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


currentInstance = newInstance()
