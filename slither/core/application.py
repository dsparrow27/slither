from functools import wraps
import logging
import os

from slither.core import scheduler, node, types, graph, proxyplugins
from zoo.libs.utils import filesystem
from zoo.core.util import zlogging, env
from zoo.core.plugin import pluginmanager
from blinker import signal as blinkerSignal

logger = zlogging.getLogger(__name__)


class EventSystem(object):

    def __init__(self):
        self._blockSignal = False
        self.graphCreated = blinkerSignal("graphCreated", doc="kwargs(sender, graph)")
        self.graphDeleted = blinkerSignal("graphDeleted", doc="kwargs(sender, graph)")
        self.nodeCreated = blinkerSignal("nodeCreated", doc="kwargs(sender, node)")
        self.nodeDeleted = blinkerSignal("nodeDeleted", doc="kwargs(sender, node)")
        self.nodeNameChanged = blinkerSignal("nodeNameChanged", doc="kwargs(sender, node, name)")
        self.nodeDirtyChanged = blinkerSignal("nodeDirtyChanged")
        self.attributeCreated = blinkerSignal("attributeCreated")
        self.attributeDeleted = blinkerSignal("attributeDeleted")
        self.attributeNameChanged = blinkerSignal("attributeNameChanged")
        self.attributeValueChanged = blinkerSignal("attributeValueChanged")
        self.schedulerNodeCompleted = blinkerSignal("schedulerNodeCompleted")
        self.schedulerNodeErrored = blinkerSignal("schedulerNodeErrored")
        self.connectionsCreated = blinkerSignal("connectionCreated")
        self.connectionsDeleted = blinkerSignal("connectionDeleted")

    def emit(self, signal: blinkerSignal, sender: callable, **kwargs):
        """Internal use only
        """
        if self._blockSignal:
            logger.debug("Signals are currently being blocked")
            return
        if not bool(signal.receivers):
            logger.debug("No Receivers for signal :{}".format(signal.name))
            return
        logger.debug("Sending signal: {}".format(signal.name))
        signal.send(sender, **kwargs)

    def blockSignals(self, func: callable):

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
    STANDARDEXECUTOR = "inProcess"

    def __init__(self):
        env.addToEnv(Registry.LIB_ENV, [os.path.join(os.path.dirname(__file__), "..", "plugins")])
        self.graphs = []
        self.events = EventSystem()
        self.registry = Registry()
        self.registry.discoverPlugins()

    def graph(self, name: str) -> graph.Graph:
        for g in self.graphs:
            if g.name == name:
                return g

    def deleteGraph(self, name: str) -> "graph.Graph":
        g = self.graph(name)
        self.graphs.remove(g)
        self.events.emit(self.events.graphDeleted, sender=self, graph=g)
        return g

    def createGraph(self, name: str) -> "graph.Graph":
        g = graph.Graph(self, name=name)
        self.graphs.append(g)
        self.events.emit(self.events.graphCreated, sender=self, graph=g)
        return g

    def createGraphFromPath(self, name: str, filePath: str) -> "graph.Graph":
        g = graph.Graph(self, name=name)
        self.events.emit(self.events.graphCreated, sender=self, graph=g)
        g.loadFromFile(filePath)
        self.graphs.append(g)
        return g


class Registry(object):
    """Specialized plugin registry which discovers via plugin json files
    """
    LIB_ENV = "SLITHER_PLUGIN_PATH"

    def __init__(self):
        self._nodeRegistry = pluginmanager.PluginManager(interface=[proxyplugins.ProxyBase],
                                                         variableName="Type")
        self._dataTypeRegistry = pluginmanager.PluginManager(interface=[types.DataType],
                                                             variableName="Type")
        self._schedulerRegistry = pluginmanager.PluginManager(interface=[scheduler.BaseScheduler],
                                                              variableName="Type")
        self._nodeInfoCache = {}
        self._dataTypeCache = {}
        self._schedulerInfoCache = {}

    @property
    def nodeTypes(self) -> dict:
        return self._nodeInfoCache

    def nodeClass(self, nodeType, graph, **kwargs):
        """Retrieves the node class for the type.

        If the registered node has a pluginPath then the node class will be searched,
        loaded from the path. Otherwise the basenode types will be return
        ie. Compound, DependencyNode etc.

        :param nodeType: The node Type
        :type nodeType: str
        """
        proxyClass, info = self.proxyNodeClass(nodeType, **kwargs)
        # temp
        if isinstance(proxyClass, proxyplugins.PXComputeNode):
            return node.ComputeNode.create(info, graph, proxyClass)
        elif isinstance(proxyClass, proxyplugins.PXCompoundNode):
            return node.Compound.create(info, graph, proxyClass)
        elif isinstance(proxyClass, proxyplugins.PXCommentNode):
            return node.Comment.create(info, graph, proxyClass)
        elif isinstance(proxyClass, proxyplugins.PXPinNode):
            return node.Pin.create(info, graph, proxyClass)
        elif isinstance(proxyClass, proxyplugins.PXInputNode):
            return node.InputNode.create(info, graph, proxyClass)
        elif isinstance(proxyClass, proxyplugins.PXOutputNode):
            return node.OutputNode.create(info, graph, proxyClass)

        raise ValueError("Failed")

    def proxyNodeClass(self, nodeType, **kwargs):
        registeredTypeInfo = self._nodeInfoCache.get(nodeType)
        if not registeredTypeInfo:
            raise ValueError(
                "Invalid node Type: {}, available: {}".format(nodeType, ",".join(self._nodeInfoCache.keys())))
        nodeClass = self._nodeRegistry.getPlugin(nodeType)
        # if we've already discovered the object once before
        # return it from the cache
        if nodeClass is None:
            raise ValueError("Failed")
        info = registeredTypeInfo["info"].copy()
        info.update(kwargs)
        return nodeClass(), info

    def dataTypeClass(self, dataType, *args, **kwargs):

        registeredTypeInfo = self._dataTypeCache.get(dataType)
        if not registeredTypeInfo:
            print(self._dataTypeRegistry.plugins.keys())
            raise ValueError("No Data type registered: {}".format(dataType))
        typeClass = self._dataTypeRegistry.getPlugin(dataType)
        # if we've already discovered the object once before
        # return it from the cache
        if typeClass:
            info = registeredTypeInfo["info"].copy()
            info.update(kwargs)
            return typeClass.create(info)
        raise ValueError("Failed")

    def schedulerClass(self, schedulerType, *args, **kwargs):

        registeredTypeInfo = self._schedulerInfoCache.get(schedulerType)
        if not registeredTypeInfo:
            raise ValueError("fail")
        typeClass = self._schedulerRegistry.getPlugin(schedulerType)
        # if we've already discovered the object once before
        # return it from the cache
        if typeClass:
            return typeClass(*args, **kwargs)
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
        schedulers = pluginInfo.get("schedulers", [])
        dataTypes = pluginInfo.get("dataTypes", [])
        for datatype in dataTypes:
            self.registerDataType(filePath, datatype)

        for n in nodes:
            self.registerNode(filePath, n)

        for dispatch in schedulers:
            self.registerScheduler(filePath, dispatch)

    def registryPluginFolder(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                self.registerPath(filePath=os.path.normpath(os.path.join(root, f)))

    def registerNode(self, path, nodeInfo):
        pluginPath = nodeInfo.get("pluginPath", "")
        if pluginPath:
            if not os.path.isabs(pluginPath):
                pluginPath = os.path.abspath(os.path.join(os.path.dirname(path), pluginPath))
            self._nodeRegistry.registerPath(pluginPath)
        else:
            proxy = self._nodeObjectByNode(nodeInfo)

            if not proxy:
                logger.warning("No Plugin class found for nodeType: {}".format(nodeInfo["type"]))
                return
            self._nodeRegistry.registerPlugin(proxy)
        info = {
            "info": nodeInfo,
            "path": pluginPath
        }

        self._nodeInfoCache[nodeInfo["type"]] = info

    def registerDataType(self, path, dataType):
        pluginPath = dataType.get("pluginPath", "")
        if not pluginPath:
            raise ValueError("No plugin path specified for path and datatype: {} - {}".format(path, dataType["type"]))
        if not os.path.isabs(pluginPath):
            pluginPath = os.path.abspath(os.path.join(os.path.dirname(path), pluginPath))
        self._dataTypeRegistry.registerPath(pluginPath)
        info = {
            "info": dataType,
            "path": pluginPath
        }
        self._dataTypeCache[dataType["type"]] = info

    def registerScheduler(self, path, schedulerInfo):
        pluginPath = schedulerInfo.get("pluginPath", "")
        if not pluginPath:
            raise ValueError(
                "No plugin path specified for path and datatype: {} - {}".format(path, schedulerInfo["type"]))
        if not os.path.isabs(pluginPath):
            pluginPath = os.path.abspath(os.path.join(os.path.dirname(path), pluginPath))
        self._schedulerRegistry.registerPath(pluginPath)
        info = {
            "info": schedulerInfo,
            "path": pluginPath
        }
        self._schedulerInfoCache[schedulerInfo["type"]] = info

    def _nodeObjectByNode(self, nodeInfo):
        # temp
        if nodeInfo.get("compound", False):
            return proxyplugins.PXCompoundNode
        elif nodeInfo.get("comment", False):
            return proxyplugins.PXCommentNode
        elif nodeInfo.get("pin", False):
            return proxyplugins.PXPinNode
        elif nodeInfo.get("input", False):
            return proxyplugins.PXInputNode
        elif nodeInfo.get("output", False):
            return proxyplugins.PXOutputNode
