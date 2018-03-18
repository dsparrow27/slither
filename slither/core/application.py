from .nodeRegistry import NodeRegistry
from .typeregistry import DataTypeRegistry
from blinker import signal


class Application(object):
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
        if self._root:
            return self._root
        self._root = self._nodeRegistry.node(type_="system")(name="system", application=self)
        # should emit event
        return self._root

    #:note:: probably shouldn't be doing this crap here
    def createNode(self, name, type_, parent=None):
        exists = self.root.child(name)
        if exists:
            # :todo: error out
            return
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


class ApplicationEvents(object):
    nodeCreated = signal("Node Created")
    nodeRemoved = signal("Node Deleted")
    nodeNameChanged = signal("Node Name Changed")
    nodeParentChanged = signal("Node parent Changed")
    attributeCreated = signal("Attribute Created", doc="Triggerd any time a new custom attribute is created")
    attributeRemoved = signal("Attribute Deleted")
    attributeValueChanged = signal("Attribute Value Changed")
    attributeNameChanged = signal("Attribute Name Changed")
    nodeProgressUpdated = signal("Node Progress Updated")
    connectionAdded = signal("Connection Added")
    connectionRemoved = signal("Connection Removed")

