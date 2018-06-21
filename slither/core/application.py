from .nodeRegistry import NodeRegistry
from .typeregistry import DataTypeRegistry
from slither.core import executor
from blinker import signal


class Application(object):
    PARALLELEXECUTOR = 0
    STANDARDEXECUTOR = 1

    def __init__(self):
        self._nodeRegistry = NodeRegistry()
        self._typeRegistry = DataTypeRegistry()
        self._events = ApplicationEvents()
        self._root = None
        self.globals = {}

    @property
    def events(self):
        return self._events

    @property
    def nodeRegistry(self):
        return self._nodeRegistry

    @property
    def typeRegistry(self):
        return self._typeRegistry

    @property
    def root(self):
        if self._root is not None:
            return self._root
        self._root = self._nodeRegistry.node(type_="system")(name="system", application=self)
        # should emit event
        return self._root

    #:note:: probably shouldn't be doing this crap here
    def createNode(self, name, type_, parent=None):
        exists = self.root.child(name)
        if exists:
            newName = name
            counter = 1
            while self.root.child(newName):
                newName = name + str(counter)
                counter += 1
            name = newName
        newNode = self._nodeRegistry.node(type_=type_)
        if newNode:
            newNode = newNode(name=name, application=self)
            if parent is None:
                self.root.addChild(newNode)
            elif parent.isCompound():
                parent.addChild(newNode)
            # should emit a event
            self.events.nodeCreated.send(newNode)
            return newNode
        # :todo error out

    def execute(self, node, executorType):
        if executorType == Application.PARALLELEXECUTOR:
            exe = executor.Parallel()
            exe.execute(node)
            return True
        elif executorType == Application.STANDARDEXECUTOR:
            exe = executor.StandardExecutor()
            exe.execute(node)
            return True
        return False


class ApplicationEvents(object):
    nodeCreated = signal("Node Created")
    nodeRemoved = signal("Node Deleted")
    nodeNameChanged = signal("Node Name Changed")
    nodeParentChanged = signal("Node parent Changed")
    selectedChanged = signal("Selection Changed")
    attributeCreated = signal("Attribute Created", doc="Triggerd any time a new custom attribute is created")
    attributeRemoved = signal("Attribute Deleted")
    attributeValueChanged = signal("Attribute Value Changed")
    attributeNameChanged = signal("Attribute Name Changed")
    nodeProgressUpdated = signal("Node Progress Updated")
    connectionAdded = signal("Connection Added")
    connectionRemoved = signal("Connection Removed")
