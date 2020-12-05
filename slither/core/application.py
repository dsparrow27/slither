import contextlib
import inspect
from functools import wraps

import logging
import os

from slither.core import dispatcher, node, types, graph
from zoo.libs.utils import filesystem, zlogging, modules, env
from blinker import signal
logger = logging.getLogger(__name__)


class EventSystem(object):

    def __init__(self):
        self._blockSignal = False
        self.graphCreated = signal("graphCreated")
        self.graphDeleted = signal("graphDeleted")
        self.nodeCreated = signal("nodeCreated")
        self.nodeDeleted = signal("nodeDeleted")
        self.nodeNameChanged = signal("nodeNameChanged")
        self.nodeDirtyChanged = signal("nodeDirtyChanged")
        self.attributeCreated = signal("attributeCreated")
        self.attributeDeleted = signal("attributeDeleted")
        self.attributeNameChanged = signal("attributeNameChanged")
        self.attributeValueChanged = signal("attributeValueChanged")
        self.schedulerNodeCompleted = signal("schedulerNodeCompleted")
        self.schedulerNodeErrored = signal("schedulerNodeErrored")

    def emit(self, signal, *args, **kwargs):
        """Internal use only
        """
        if self._blockSignal:
            logger.debug("Signals are currently being blocked")
            return
        if not bool(signal.receivers):
            logger.debug("No Receivers for signal :{}".format(signal.name))
            return

        signal.send(*args, **kwargs)

    def blockSignals(self, func):

        @wraps(func)
        def _block(*args, **kwargs):
            try:
                self._blockSignal = True
                return func(*args, **kwargs)
            finally:
                self._blockSignal = False

        return _block


class Application(object):
    PARALLELEXECUTOR = "parallel"
    STANDARDEXECUTOR = "serial"

    def __init__(self):
        env.addToEnv(Registry.LIB_ENV, [os.path.join(os.path.dirname(__file__), "..", "plugins")])
        self.graphs = []
        self.events = EventSystem()
        self.registry = Registry()
        self.registry.discoverPlugins()

    def graph(self, name):
        for g in self.graphs:
            if g.name == name:
                return g

    def deleteGraph(self, name):
        g = self.graph(name)
        self.graphs.remove(g)
        self.events.emit(self.events.graphDeleted, graph=g)
        return g

    def createGraph(self, name):
        g = graph.Graph(self, name=name)
        self.graphs.append(g)
        self.events.emit(self.events.graphCreated, graph=g)
        return g


class Registry(object):
    """Specialized plugin registry which discovers via plugin json files
    """
    LIB_ENV = "SLITHER_PLUGIN_PATH"

    def __init__(self):
        self.nodes = {}
        self.dataTypes = {}
        self.dispatchers = {}

    def nodeClass(self, nodeType, graph, **kwargs):
        """Retrieves the node class for the type.

        If the registered node has a pluginPath then the node class will be searched,
        loaded from the path. Otherwise the basenode types will be return
        ie. Compound, DependencyNode etc.

        :param nodeType: The node Type
        :type nodeType: str
        """
        registeredTypeInfo = self.nodes.get(nodeType)
        if not registeredTypeInfo:
            raise ValueError("fail {}".format(nodeType))
        # if we've already discovered the object once before
        # return it from the cache
        cachedObject = registeredTypeInfo["class"]
        if cachedObject:
            info = registeredTypeInfo["info"].copy()
            info.update(kwargs)
            logger.debug("Creating Node : {}".format(nodeType))
            return cachedObject.create(info, graph)
        raise ValueError("Failed")

    def dataTypeClass(self, dataType, *args, **kwargs):
        registeredTypeInfo = self.dataTypes.get(dataType)
        if not registeredTypeInfo:
            raise ValueError("fail")
        # if we've already discovered the object once before
        # return it from the cache
        cachedObject = registeredTypeInfo["class"]
        if cachedObject:
            info = registeredTypeInfo["info"].copy()
            info.update(kwargs)
            return cachedObject.create(info)
        raise ValueError("Failed")

    def dispatcherClass(self, dispatcherType, *args, **kwargs):
        registeredTypeInfo = self.dispatchers.get(dispatcherType)
        if not registeredTypeInfo:
            raise ValueError("fail")
        # if we've already discovered the object once before
        # return it from the cache
        cachedObject = registeredTypeInfo["class"]
        if cachedObject:
            return cachedObject(*args, **kwargs)
        raise ValueError("Failed")

    def discoverPlugins(self):
        paths = [i for i in os.getenv(Registry.LIB_ENV, "").split(os.pathsep) if i]
        for path in paths:
            if not os.path.exists(path):
                continue
            if os.path.isfile(path):
                self.registerPath(path)
            elif os.path.isdir(path):
                self.registryPluginFolder(path)
            else:
                logger.warning("Specified path is not valid file or directory: {}".format(path))

    def registerPath(self, filePath):
        if not filePath.endswith(".slplugin"):
            return
        pluginInfo = filesystem.loadJson(filePath)
        nodes = pluginInfo.get("nodes", [])
        dispatchers = pluginInfo.get("dispatchers", [])
        dataTypes = pluginInfo.get("dataTypes", [])
        for datatype in dataTypes:
            self.registerDataType(filePath, datatype)

        for n in nodes:
            self.registerNode(filePath, n)

        for dispatch in dispatchers:
            self.registerDispatcher(filePath, dispatch)

    def registryPluginFolder(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                self.registerPath(filePath=os.path.normpath(os.path.join(root, f)))

    def registerNode(self, path, nodeInfo):
        pluginPath = nodeInfo.get("pluginPath", "")
        pluginObj = None
        if pluginPath:
            if not os.path.isabs(pluginPath):
                pluginPath = os.path.abspath(os.path.join(os.path.dirname(path), pluginPath))
            module = modules.importModule(modules.asDottedPath(pluginPath))
            for dataClass in modules.iterMembers(module, predicate=inspect.isclass):
                if dataClass[1].Type == nodeInfo["type"]:
                    pluginObj = dataClass[1]
                    break

        if pluginObj is None:
            pluginObj = self._nodeObjectByNode(nodeInfo)

        info = {
            "info": nodeInfo,
            "class": pluginObj,
            "path": pluginPath
        }

        self.nodes[nodeInfo["type"]] = info

    def registerDataType(self, path, dataType):
        pluginPath = dataType.get("pluginPath", "")
        if not pluginPath:
            raise ValueError("No plugin path specified for path and datatype: {} - {}".format(path, dataType["type"]))
        if not os.path.isabs(pluginPath):
            pluginPath = os.path.abspath(os.path.join(os.path.dirname(path), pluginPath))
        pluginObj = modules.importModule(pluginPath)
        for dataClass in modules.iterSubclassesFromModule(pluginObj, types.DataType):
            if dataClass.Type == dataType["type"]:
                break
        else:
            raise ValueError("No dataType subclass found: {} - {}".format(path, dataType["type"]))
        info = {
            "info": dataType,
            "class": dataClass,
            "path": pluginPath
        }
        types.__dict__[dataType["type"]] = dataClass
        self.dataTypes[dataType["type"]] = info

    def registerDispatcher(self, path, dispatcherInfo):
        pluginPath = dispatcherInfo.get("pluginPath", "")
        if not pluginPath:
            raise ValueError(
                "No plugin path specified for path and datatype: {} - {}".format(path, dispatcherInfo["type"]))
        if not os.path.isabs(pluginPath):
            pluginPath = os.path.abspath(os.path.join(os.path.dirname(path), pluginPath))
        pluginObj = modules.importModule(pluginPath)
        for dataClass in modules.iterSubclassesFromModule(pluginObj, dispatcher.BaseDispatcher):
            if dataClass.Type == dispatcherInfo["type"]:
                break
        else:
            raise ValueError("No dispatcher subclass found: {} - {}".format(path, dispatcherInfo["type"]))
        info = {
            "info": dispatcherInfo,
            "class": dataClass,
            "path": pluginPath
        }
        self.dispatchers[dispatcherInfo["type"]] = info

    def _nodeObjectByNode(self, nodeInfo):
        if nodeInfo.get("compound", False):
            return node.Compound
        elif nodeInfo.get("comment", False):
            return node.Comment
        elif nodeInfo.get("pin", False):
            return node.Pin
        return node.PythonNode
