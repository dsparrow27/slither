import pprint


from slither.core import node, errors, scheduler, attribute
from zoo.libs.utils import filesystem, path
from zoo.core.util import zlogging
logger = zlogging.getLogger(__name__)


class Graph(object):
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
        _root.nodeUI["label"] = "root"
        # mark the root as internal and locked so it can't be deleted.
        _root.isLocked = True
        _root.isInternal = True
        self._root = _root

        self.application.events.emit(self.application.events.nodeCreated, sender=self, node=_root)
        return self._root

    def saveToFile(self, filePath, node=None):
        data = self.serialize(node)
        outputPath = path.withExtension(filePath, ".slgraph")
        try:
            filesystem.saveJson(data, outputPath)
        except TypeError:
            pprint.pprint(data)
            raise
        return outputPath

    def serialize(self, node=None):
        n = node or self.root
        data = n.serialize()
        connections = []
        for connection in self.connections:
            connections.append(dict(
                source=connection["source"].name,
                destination=connection["destination"].name,
                input=connection["input"].name(),
                output=connection["output"].name()
            ))
        data["connections"] = connections
        return data

    def execute(self, n, executorType):
        job = scheduler.Job("JOB: {}".format(n.name), self.application)
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
            root = self.root
            newNodes[data["name"]] = root
            root.deserialize(data, includeChildren=False)
            root.setDirty(True)
            for child in children:
                newNode = self.createNode(child["name"], child["type"], parent=root)
                for i, n in newNode.deserialize(child).items():
                    newNodes[i] = n
                # we need to deal with connections so first create a map between the old and the new
                newNodes[child["name"]] = newNode
                if isinstance(newNode, node.ComputeNode):
                    newNode.setDirty(True)
            missingConnections = []
            missingNodes = []
            for connection in connections:
                sourceNode = newNodes.get(connection["source"])
                destinationNode = newNodes.get(connection["destination"])
                if sourceNode is None or destinationNode is None:
                    missingNodes.append(connection)
                    continue

                sourceAttr = sourceNode.attribute(connection["output"])
                destAttr = destinationNode.attribute(connection["input"])
                if sourceAttr is None or destAttr is None:
                    missingConnections.append(connection)
                    continue
                sourceAttr.connect(destAttr)
            if missingNodes:
                logger.warning("Couldn't find nodes "
                               "due to missing names: {}".format(str(missingNodes)))
            if missingConnections:
                logger.warning("Couldn't create the following connections "
                               "due to missing names: {}".format(str(missingConnections)))
            return {"nodes": newNodes,
                    "missingConnections": missingConnections}

        return _load(data)

    def createConnection(self, source, destination):
        connection = {"source": source.node, "destination": destination.node,
                      "input": destination, "output": source}
        self.connections.append(connection)
        self.application.events.emit(self.application.events.connectionsCreated,
                                     sender=self,
                                     sourcePlug=source,
                                     destinationPlug=destination
                                     )
        return connection

    def removeConnection(self, source, destination):
        if destination.upstream != source:
            return False
        destination.disconnect()
        for index, conn in enumerate(self.connections):
            if conn["input"] == destination and conn["output"] == source \
                    and conn["source"] == source and conn["destination"] == destination:
                self.connections.pop(index)
                self.application.events.emit(self.application.events.connectionDeleted,
                                             sender=self,
                                             sourcePlug=source,
                                             destinationPlug=destination
                                             )
                break

    def createNode(self, name, type_, parent=None):
        @self.application.events.blockSignals
        def _create(name, type_, parent):
            parent = parent if parent is not None else self.root
            exists = parent.child(name)
            if exists is not None:
                newName = name
                counter = 1
                while parent.child(newName) is not None:
                    newName = name + str(counter)
                    counter += 1
                name = newName
            newNode = self.application.registry.nodeClass(type_, name=name, graph=self)

            if newNode is not None:
                parent.addChild(newNode)
                return newNode

        result = _create(name, type_, parent)
        if result is not None:
            self.application.events.emit(self.application.events.nodeCreated, sender=self, node=result)
        return result

    def removeNode(self, child, parent):
        if child.isLocked or child.isInternal:
            return False

        if child in self:
            if isinstance(child, node.DependencyNode):
                child.disconnectAll()
            parent.children.remove(child)
            self.application.events.emit(self.application.events.nodeDeleted, sender=self, node=child)
            return True
        return False
