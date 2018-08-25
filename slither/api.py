import logging, os, sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Slither")
logger.addHandler(logging.NullHandler())

NODE_LIB_ENV = "SLITHER_NODE_LIB"
TYPE_LIB_ENV = "SLITHER_TYPE_LIB"

# :todo piss this off
root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(root, "thirdparty"))
pluginBase = os.path.join(root, "slither", "plugins")
os.environ[NODE_LIB_ENV] = os.path.join(pluginBase, "nodes")
os.environ[TYPE_LIB_ENV] = os.path.join(pluginBase, "datatypes")

from slither.core import application as _application

currentInstance = None
instances = []


def newInstance(current=True):
    global currentInstance, instances

    app = _application.Application()
    instances.append(app)
    if current:
        currentInstance = app
    return app
currentInstance = newInstance()