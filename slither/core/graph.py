import logging
import os

from slither.core import dispatcher, node, types, errors
from zoo.libs.plugin import pluginmanager
from zoo.libs.utils import filesystem, zlogging

logger = zlogging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class Graph(object):
    PARALLELEXECUTOR = 0
    STANDARDEXECUTOR = 1
    NODE_LIB_ENV = "SLITHER_NODE_LIB"
    TYPE_LIB_ENV = "SLITHER_TYPE_LIB"
    DISPATCHER_LIB_ENV = "DISPATCHER_LIB"

    def __init__(self):
        self.nodeRegistry = pluginmanager.PluginManager(node.BaseNode, variableName="Type")
        self.typeRegistry = pluginmanager.PluginManager(types.DataType, variableName="Type")
        self.dispatchers = pluginmanager.PluginManager(dispatcher.BaseDispatcher, variableName="Type")
        self._root = None
        self.variables = {}
        self.nodeIds = set()
        self.connections = []

    def initialize(self):
        self.dispatchers.registerPaths(os.environ[self.DISPATCHER_LIB_ENV].split(os.pathsep))
        self.typeRegistry.registerPaths(os.environ[self.TYPE_LIB_ENV].split(os.pathsep))
        types.__dict__.update(self.typeRegistry.plugins.items())

        self.nodeRegistry.registerPaths(os.environ[self.NODE_LIB_ENV].split(os.pathsep))
        # add the compound base node
        self.nodeRegistry.registerPlugin(node.Compound)
        self.nodeRegistry.registerPlugin(node.Pin)
        self.nodeRegistry.registerPlugin(node.Comment)

    def shutdown(self):
        pass

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def dataType(self, typeName):
        return self.typeRegistry.getPlugin(typeName)

    @property
    def root(self):
        if self._root is not None:
            return self._root
        self._root = self.nodeRegistry.loadPlugin("compound", name="Root", graph=self)
        self._root.id = self._generateNewNodeId()
        # mark the root as internal and locked so it can't be deleted.
        self._root.isLocked = True
        self._root.isInternal = True
        return self._root

    def saveToFile(self, filePath, node=None):
        data = self.serialize(node)
        filesystem.saveJson(data, filePath)
        return os.path.exists(filePath)

    def serialize(self, node=None):
        n = node or self.root
        data = n.serialize()
        data["connections"] = self.connections
        return data

    def execute(self, n, executorType):
        logger.debug("Starting execution")
        if executorType == Graph.PARALLELEXECUTOR:
            exe = self.dispatchers.getPlugin("Parallel")(self)
        elif executorType == Graph.STANDARDEXECUTOR:
            exe = self.dispatchers.getPlugin("Serial")(self)
        else:
            raise NotImplementedError("No Dispatcher of type: {}".format(str(executorType)))
        try:
            exe.execute(n)
            logger.debug("Finished Executing graph")
        except Exception:
            logger.error("Failed to execute Graph",
                         exc_info=True)
            return False
        return True

    def load(self, data):
        # data can be a fraction full graph or it maybe start from the graph root system
        newNodes = {}
        connections = data.get("connections", [])
        if data["name"] == "Root":
            children = data.get("children", [])
            newNodes[data["id"]] = self.root
        else:
            children = [data]

        root = self.root
        root.deserialize(data, includeChildren=False)

        for child in children:
            newNode = self.createNode(child["name"], child["type"], parent=root)
            for i, n in newNode.deserialize(child).items():
                newNodes[i] = n
            # we need to deal with connections so first create a map between the old and the new
            newNodes[child["id"]] = newNode
        missingConnections = []
        missingNodes = []
        for connection in connections:
            sourceNode = newNodes.get(connection["source"])
            destinationNode = newNodes.get(connection["destination"])
            if sourceNode is None or destinationNode is None:
                missingNodes.append(connection)
                continue
            sourceAttr = sourceNode.attributeById(connection["output"])
            destAttr = destinationNode.attributeById(connection["input"])
            if sourceAttr is None or destAttr is None:
                missingConnections.append(connection)
                continue
            self.createConnection(sourceAttr, destAttr)

        if missingNodes:
            logger.warning("Couldn't find nodes "
                           "due to missing ids: {}".format(str(missingNodes)))
        if missingConnections:
            logger.warning("Couldn't create the following connections "
                           "due to missing ids: {}".format(str(missingConnections)))
        return {"nodes": newNodes,
                "missingConnections": missingConnections}

    def removeConnection(self, source, destination):
        if destination.upstream != source:
            return False
        destination.upstream = None
        for index, conn in enumerate(self.connections):
            if conn["input"] == destination.id and conn["output"] == source.id \
                    and conn["source"] == source.id and conn["destination"] == destination:
                self.connections.pop(index)

    def createConnection(self, source, destination):
        if not source.canConnect(destination):
            raise errors.AttributeCompatiblityError(source, destination)
        if destination.upstream is not None:
            raise errors.AttributeAlreadyConnected(source, destination)
        logger.debug("Creating connection between: {}->{}".format(source.fullName(), destination.fullName()))
        print("Creating connection between: {}->{}".format(source.fullName(), destination.fullName()))
        destination.upstream = source
        self.connections.append({"source": source.node.id, "destination": destination.node.id,
                                 "input": destination.id, "output": source.id})

    def createNode(self, name, type_, parent=None):
        parent = parent if parent is not None else self.root
        exists = self.root.child(name)
        if exists:
            newName = name
            counter = 1
            while self.root.child(newName):
                newName = name + str(counter)
                counter += 1
            name = newName
        newNode = self.nodeRegistry.loadPlugin(type_, name=name, graph=self)
        if newNode is not None:
            newNode.id = self._generateNewNodeId()
            parent.addChild(newNode)
            # should emit a event
            return newNode

    def _generateNewNodeId(self):
        newId = 0 if not self.nodeIds else max(self.nodeIds) + 1
        self.nodeIds.add(newId)
        return newId

    def removeNode(self, child, parent):
        if child.isLocked or child.isInternal:
            return False

        if child in self:
            if isinstance(child, node.DependencyNode):
                child.disconnectAll()
            self.nodeIds.remove(child.id)
            parent.children.remove(child)
            return True
        return False
