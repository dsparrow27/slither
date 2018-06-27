import logging, os, sys

NODE_LIB_ENV = "SLITHER_NODE_LIB"
TYPE_LIB_ENV = "SLITHER_TYPE_LIB"

# :todo piss this off
root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(root, "thirdparty"))
pluginBase = os.path.join(root, "slither", "plugins")
os.environ[NODE_LIB_ENV] = os.path.join(pluginBase, "nodes")
os.environ[TYPE_LIB_ENV] = os.path.join(pluginBase, "datatypes")

from slither.core import application as _application

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Slither")
logger.addHandler(logging.NullHandler())

_currentApplication = None
def initialize():
    global _currentApplication
    if _currentApplication:
        return _currentApplication

    _currentApplication = _application.Application()
    return _currentApplication

currentInstance = initialize()

from slither.core.attribute import InputDefinition, OutputDefinition
from slither.core import ktypes