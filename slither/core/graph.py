import os
import pprint
import logging
import time

from slither.core import node, errors, scheduler, attribute
from zoo.libs.utils import filesystem, zlogging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Graph(object):
    NODE_LIB_ENV = "SLITHER_NODE_LIB"
    TYPE_LIB_ENV = "SLITHER_TYPE_LIB"
    scheduler_LIB_ENV = "scheduler_LIB"

    def __init__(self, app, name):
        """
        :param app: The slither application instance
        :type app: :class:`slither.core.application.Application`
        :param name: Graph name
        :type name: str
        """
        self.application = app
        self.name = name
        self._root = None
        self.variables = {}
        self.nodeIds = set()
        self.connections = []

    def shutdown(self):
        pass

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def dataType(self, typeName):
        return self.application.registry.dataTypeClass(typeName)

    @property
    def root(self):
        if self._root is not None:
            return self._root
        _root = self.application.registry.nodeClass("compound", graph=self, name=self.name or "world")
        _root.id = self._generateNewNodeId()
        _root.nodeUI["label"] = "root"
        # mark the root as internal and locked so it can't be deleted.
        _root.isLocked = True
        _root.isInternal = True
        # execDef = attribute.AttributeDefinition(name="execute",
        #                                         input=False,
        #                                         output=True,
        #                                         type_=self.application.registry.dataTypeClass("kMulti"),
        #                                         required=True, array=True,
        #                                         doc="",
        #                                         internal=True)
        # _root.createAttribute(execDef)
        self._root = _root
        self.application.events.emit(self.application.events.nodeCreated, sender=self, node=_root)
        return self._root

    def saveToFile(self, filePath, node=None):
        data = self.serialize(node)
        pathSplit = filePath.split(os.path.extsep)
        outputPath = filePath
        if pathSplit[-1] != ".slgraph":
            outputPath = pathSplit[0] + ".slgraph"
        try:
            filesystem.saveJson(data, outputPath)
        except TypeError:
            pprint.pprint(data)
            raise
        return outputPath

    def serialize(self, node=None):
        n = node or self.root
        data = n.serialize()
        data["connections"] = self.connections
        return data

    def execute(self, n, executorType):
        job = scheduler.Job("testJob", self.application)
        job.submit(n, executorType)
        while not job.isCompleted():
            job.poll()
        logger.debug("Finished Executing graph")
        return job

    def loadFromFile(self, path):
        self.load(filesystem.loadJson(path))

    def load(self, data):
        @self.application.events.blockSignals
        def _load(data):
            logger.debug("Starting graph loading")
            # data can be a fraction full graph or it maybe start from the graph root system
            newNodes = {}
            connections = data.get("connections", [])
            children = data.get("children", [])
            newNodes[data["id"]] = self.root

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

        return _load(data)

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
        destination.upstream = source
        connection = {"source": source.node.id, "destination": destination.node.id,
                      "input": destination.id, "output": source.id}
        self.connections.append(connection)
        return connection

    def createNode(self, name, type_, parent=None):
        @self.application.events.blockSignals
        def _create(name, type_, parent):
            parent = parent if parent is not None else self.root
            exists = self.root.child(name)
            if exists:
                newName = name
                counter = 1
                while self.root.child(newName):
                    newName = name + str(counter)
                    counter += 1
                name = newName
            newNode = self.application.registry.nodeClass(type_, name=name, graph=self)
            if newNode is not None:
                newNode.id = self._generateNewNodeId()
                parent.addChild(newNode)

                return newNode

        result = _create(name, type_, parent)
        if result is not None:
            self.application.events.emit(self.application.events.nodeCreated, sender=self, node=result)
        return result

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
            self.application.events.emit(self.application.events.nodeDeleted, sender=self, node=child)
            return True
        return False
