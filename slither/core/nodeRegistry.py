import inspect
import os
import logging

from slither.core import modules
from slither.core import node
from slither.core import compound
from slither.core import classtypes

logger = logging.getLogger(__name__)


class NodeRegistry(object):
    __metaclass__ = classtypes.Singleton
    NODE_LIB_ENV = "SLITHER_NODE_LIB"

    nodes = {}

    def __init__(self):
        self.registerFromEnv(NodeRegistry.NODE_LIB_ENV)
        NodeRegistry.nodes["system"] = compound.Compound

    @classmethod
    def node(cls, type_):
        """Returns the appropriate node instance based on the type requested.
        :param type_: The type of node to return
        :type type_: str
        :rtype: Node instance
        """
        if type_ in cls.nodes:
            return cls.nodes[type_]

    @classmethod
    def registerFromEnv(cls, env):
        paths = os.environ.get(env)
        if not paths:
            raise ValueError("Cannot find environmentVariable -> %s" % env)
        for p in paths.split(os.pathsep):
            if p.endswith(".pyc"):
                continue
            elif os.path.isdir(p):
                cls.registerByPackage(p)
                continue
            elif os.path.isfile(p):
                importedModule = modules.importModule(p)
                if importedModule:
                    cls.registerByModule(importedModule)
                    continue
            #
            # if p:
            #     try:
            #         importedModule = modules.importModule(p)
            #     except Exception:
            #         logger.error("Failed to import module {}".format(p), exc_info=True)
            # if importedModule:
            #     cls.registerByModule(importedModule)
            #     continue
            # cls.registerByPackage(p)


    @classmethod
    def registerNode(cls, classObject):
        name = classObject.__name__
        if name not in cls.nodes:
            cls.nodes[name] = classObject

    @classmethod
    def registerByModule(cls, module):
        if inspect.ismodule(module):
            for member in modules.iterMembers(module, predicate=inspect.isclass):
                try:
                    if issubclass(member[1], node.BaseNode) and member[1] != node.BaseNode:
                        cls.registerNode(member[1])
                except Exception:
                    logger.error("Failed to initialize Node {}".format(member[0]), exc_info=True)
    @classmethod
    def registerByPackage(cls, pkg):
        visited = set()
        for subModule in modules.iterModules(pkg):
            filename = os.path.splitext(os.path.basename(subModule))[0]
            if filename.startswith("__") or filename in visited:
                continue
            visited.add(filename)
            subModuleObj = modules.importModule(subModule)
            if subModuleObj:
                cls.registerByModule(subModuleObj)
