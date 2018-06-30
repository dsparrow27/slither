import copy
import uuid
from blinker import signal
from slither.core import attribute
from slither.core import service


class NodeEvents(object):
    kAddAttribute = 0
    kAttributeNameChanged = 1
    kNodeNameChanged = 2
    kRemoveAttribute = 3
    kAddConnection = 4
    kRemoveConnection = 5
    kValueChanged = 6
    kSelectionChanged = 7
    kProgressUpdated = 8
    kParentChanged = 9

    def __init__(self):
        # {callbackType: {"event": Signal,
        # "ids": {id: func}
        #               }
        # }
        self.callbacks = {}

    def emitCallback(self, callbackType, **kwargs):
        existing = self.callbacks.get(callbackType)
        if existing is None:
            return
        ids = existing["ids"]
        if not ids:
            return
        existing["event"].send(self.emitCallback, **kwargs)

    def addCallback(self, callbackType, func):
        existingCallback = self.callbacks.get(callbackType)

        # we have existing callback for the type so just connect to it
        callbackId = uuid.uuid4()
        if existingCallback is not None:
            existingCallback["event"].connect(func)
            existingCallback["ids"].update({callbackId: func})
        else:
            # no existing callback so create One
            event = signal(callbackType)
            event.connect(func, sender=self.emitCallback)
            self.callbacks[callbackType] = {"event": event,
                                            "ids": {callbackId: func}}
        return callbackId

    def removeCallback(self, callbackId):
        for eventInfo in self.callbacks.values():
            ids = eventInfo["ids"]
            func = ids.get(callbackId)
            if func is not None:
                eventInfo["event"].disconnect(func)
                del ids[callbackId]
                return True
        return False


class NodeMeta(type):
    @staticmethod
    def __new__(cls, className, bases, classDict):
        attrsToRename = []
        for name, attr in iter(classDict.items()):
            if isinstance(attr, attribute.AttributeDefinition):
                attr.setName(name)
                attrsToRename.append(attr)
        for attr in attrsToRename:
            name = attr.name
            newName = "_%s" % name if not name.startswith("_") else name
            old = classDict.pop(name)
            classDict[newName] = old
        return super(NodeMeta, cls).__new__(cls, className, bases, classDict)


class BaseNode(object):
    __metaclass__ = NodeMeta
    category = ""
    tags = set()
    documentation = ""

    def __init__(self, name, application):
        self.application = application
        self.events = NodeEvents()
        self.name = name
        self.attributes = []
        self.metadata = {}
        self.isLocked = False
        self.isLocked = False
        self.isInternal = False
        self._selected = False
        self._parent = None
        self._progress = 0
        attrDef = attribute.InputDefinition(type_=None,
                                                    default=None,
                                                    required=False, array=True,
                                                    doc="Node Level dependencies")
        attrDef.name = "Dependencies"
        attr = service.createAttribute(self, attrDef)
        self.addAttribute(attr)

        for name, attrDef in iter(self.__class__.__dict__.items()):
            if isinstance(attrDef, attribute.AttributeDefinition):
                attr = service.createAttribute(self, attrDef)
                self.addAttribute(attr)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected != value:
            self._selected = value
            self.events.emitCallback(NodeEvents.kSelectionChanged, node=self, state=value)

    def execute(self):
        pass

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.events.emitCallback(NodeEvents.kProgressUpdated, node=self, progress=value)

    @staticmethod
    def isCompound():
        """StaticMethod, Returns whether or not this node is a compound.
        :return: True if a compound.
        :rtype: bool
        """
        return False

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return other is not None and self.name == other.name

    def __ne__(self, other):
        return other is not None and self.name != other.name

    def __setattr__(self, name, value):
        if hasattr(self, "attributes"):
            attr = self.attribute(name)
            if attr is not None:
                isAttr = isinstance(attr, attribute.Attribute)
                if isAttr and isinstance(value, attribute.Attribute):
                    attr.connectUpstream(value)
                else:
                    attr.setValue(value)
                return
        super(BaseNode, self).__setattr__(name, value)

    def __getattr__(self, name):
        """Returns the attribute on the current node if it exists.
        :param name: The name of the attribute
        :type name: str
        :rtype: Attribute
        """
        attr = self.attribute(name)
        if attr is not None:
            return attr
        return super(BaseNode, self).__getattribute__(name)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if self._parent != node:
            self._parent = node
            self.events.emitCallback(NodeEvents.kParentChanged, node=self, parent=node)

    def type(self):
        """Returns the type of this node
        :rtype: string
        """
        return self.__class__.__name__

    def setName(self, name):
        """Sets the name of the node if the name already exists in the graph then a number will be append
        :param name: The name of the node.
        :type name: str
        :rtype: str
        """
        if self.name != name:
            self.name = name
            self.events.emitCallback(NodeEvents.kNodeNameChanged, node=self, name=self)

        return self.name

    def fullName(self):
        """Returns the full path name of the node eg. |parent|currentNode
        :rtype str
        """
        if self.parent:
            return "|".join([self.parent.fullName(), self.name])
        return self.name

    def attribute(self, name):
        for attr in self.iterAttributes():
            if attr.name() == name:
                return attr

    def addAttribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes.append(attribute)
            self.events.emitCallback(NodeEvents.kAddAttribute, node=self, attribute=attribute)
            return True
        return False

    def createAttribute(self, attributeDefinition):
        attr = service.createAttribute(self, attributeDefinition)
        name = attr.name()
        className = "_%s" % name if not name.startswith("_") else name
        super(BaseNode, self).__setattr__(className, attributeDefinition)
        self.addAttribute(attr)
        return attr

    def removeAttribute(self, name):
        for i in range(len(self.attributes)):
            attr = self.attributes[i]
            if attr.name() == name:
                self.events.emitCallback(NodeEvents.kRemoveAttribute, node=self, attribute=attr)
                del self.attributes[i]
                return True
        return False

    def hasAttribute(self, name):
        return True if self.attribute(name) else False

    def inputs(self):
        return list(self.iterInputs())

    def attributeCount(self):
        return len(self.attributes)

    def iterAttributes(self):
        return iter(self.attributes)

    def outputs(self):
        return list(self.iterOutputs())

    def depth(self):
        index = 0
        if self.parent:
            index += self.parent.depth + 1
        return index

    def iterInputs(self):
        for i in self.attributes:
            if i.isInput():
                yield i

    def iterOutputs(self):
        for i in self.attributes:
            if i.isOutput():
                yield i

    def hasOutputs(self):
        for attr in self.iterAttributes():
            if attr.isOutput():
                return True
        return False

    def hasInputs(self):
        for attr in self.iterAttributes():
            if attr.isInput():
                return True
        return False

    def upstreamNodes(self):
        return service.upstreamNodes(self)

    def downStreamNodes(self):
        return service.downStreamNodes(self)

    def siblings(self):
        return service.siblingNodes(self)

    def disconnectAll(self):
        for attr in self.iterAttributes():
            attr.disconnect()

    def serialize(self):
        data = {"name": self.name,
                "parent": self.parent.fullName() if self.parent else None,
                "attributes": [i.serialize() for i in self.attributes]
                }
        return data

    def clone(self):
        copy.deepcopy(self)
