from .registry import NodeRegistry
from .registry import DataTypeRegistry
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

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

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
        self._root = self._nodeRegistry.loadPlugin("Compound", name="Root System", application=self)
        # mark the root as internal and locked so it can't be deleted.
        self._root.isLocked = True
        self._root.isInternal = True
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
        newNode = self._nodeRegistry.loadPlugin(type_, name=name, application=self)
        if newNode is not None:
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
    def __init__(self):
        self.nodeCreated = signal("Node Created")
        self.nodeRemoved = signal("Node Deleted")
        self.selectedChanged = signal("Selection Changed")
    # nodeNameChanged = signal("Node Name Changed")
    # nodeParentChanged = signal("Node parent Changed")
    # attributeCreated = signal("Attribute Created", doc="Triggerd any time a new custom attribute is created")
    # attributeRemoved = signal("Attribute Deleted")
    # attributeValueChanged = signal("Attribute Value Changed")
    # attributeNameChanged = signal("Attribute Name Changed")
    # nodeProgressUpdated = signal("Node Progress Updated")
    # connectionAdded = signal("Connection Added")
    # connectionRemoved = signal("Connection Removed")
