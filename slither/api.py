import logging, os, sys

NODE_LIB_ENV = "SLITHER_NODE_LIB"
TYPE_LIB_ENV = "SLITHER_TYPE_LIB"

# :todo piss this off
root = os.path.realpath(os.path.dirname(__file__), "..")
sys.path.append(os.path.join(root, "thirdparty"))
pluginBase = os.path.join(root, "slither", "plugins")
os.environ[NODE_LIB_ENV] = os.path.join(pluginBase, "nodes")
os.environ[TYPE_LIB_ENV] = os.path.join(pluginBase, "datatypes")

from .core import application as _application

_currentApplication = None

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def initialize():
    global _currentApplication
    current = currentInstance()
    if current:
        return current

    _currentApplication = _application.Application()
    return _currentApplication


def currentInstance():
    global _currentApplication
    if _currentApplication:
        return _currentApplication
