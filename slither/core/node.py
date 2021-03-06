import uuid
from blinker import signal
from slither.core import attribute
import logging
from slither.core import service

logger = logging.getLogger(__name__)


class NodeEvents(object):
    kAddAttribute = 0
    kAttributeNameChanged = 1
    kAttributeValueChanged = 2
    kNodeNameChanged = 3
    kRemoveAttribute = 4
    kAddConnection = 5
    kRemoveConnection = 6
    kValueChanged = 7
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
        kwargs["eventType"] = callbackType
        ev = existing["event"]
        if bool(ev.receivers):
            ev.send(self, **kwargs)

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
            event.connect(func, sender=self)
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
        self.isInternal = False
        self._selected = False
        self._parent = None
        self._progress = 0
        attrDef = attribute.AttributeDefinition(isInput=True,
                                                isOutput=True,
                                                type_=list,
                                                default=list(),
                                                required=False, array=True,
                                                doc="Node Level dependencies")
        attrDef.name = "Dependencies"
        self.createAttribute(attrDef)

        for name, attrDef in iter(self.__class__.__dict__.items()):
            if isinstance(attrDef, attribute.AttributeDefinition):
                self.createAttribute(attrDef)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected != value:
            self._selected = value
            self.application.events.emitCallback(self.application.events.kSelectedChanged,
                                                 node=self, state=value)

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
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

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
        if self.hasAttribute(attributeDefinition.name):
            logger.error("Can't create attribute: {} because it already exists".format(attributeDefinition.name))
            raise ValueError("Name -> {} already exists".format(attributeDefinition.name))
        logger.debug("Creating Attribute: {} on node: {}".format(attributeDefinition.name,
                                                                 self.name))
        if attributeDefinition.isArray:
            newAttribute = attribute.ArrayAttribute(attributeDefinition, node=self)
        elif attributeDefinition.isCompound:
            newAttribute = attribute.CompoundAttribute(attributeDefinition, node=self)
        else:
            newAttribute = attribute.Attribute(attributeDefinition, node=self)

        name = newAttribute.name()
        className = "_{}".format(name) if not name.startswith("_") else name
        super(BaseNode, self).__setattr__(className, attributeDefinition)
        self.addAttribute(newAttribute)
        return newAttribute

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
        nodes = []
        for input_ in self.iterInputs():
            if input_.hasUpstream():
                nodes.append(input_.upstream.node)
        return nodes

    def downStreamNodes(self):
        nodes = []
        if self.parent:
            children = self.parent.children
            for i in children:
                if self in i.upstreamNodes():
                    nodes.append(i)
        return nodes

    def siblings(self):
        """Finds and returns all the siblings nodes under the node parent

        :return:
        :rtype: list(Basenode instance)
        """
        nodes = []
        if self.parent:
            for i in self.parent:
                if i != self:
                    nodes.append(i)
        return nodes

    def disconnectAll(self):
        for attr in self.iterAttributes():
            attr.disconnect()

    def serialize(self):
        data = {"name": self.name,
                "parent": self.parent.fullName() if self.parent else None,
                "attributes": [i.serialize() for i in self.attributes],
                "isCompound": self.isCompound()
                }
        return data

    def copyOutputData(self, outputs):
        """Copies the output data on to this nodes output values.

        :param outputs:
        :type outputs:
        :return:
        :rtype:
        """
        for name, value in iter(outputs.items()):
            attr = self.attribute(name)
            if attr is not None:
                attr.setValue(value)


class Compound(BaseNode):
    """The Compound class encapsulates a set of child nodes, which can include other compounds.
    We provide methods to query the children nodes of the current compound.
    """

    def __init__(self, name, application):
        """
        :param name: The name that this node will have, if the name already exist a number we be appended.
        :type name: str
        """
        super(Compound, self).__init__(name, application=application)
        self.children = []

    def setSelected(self, selected):
        """Overridden to select/de-select all children if this compound gets the selection changed

        :param selected: selection value True or False
        :type selected: bool
        """
        self.selected = selected
        for child in self.children:
            child.setSelected(selected)

    @staticmethod
    def isCompound():
        return True

    def __len__(self):
        """returns the number of child nodes for this compound

        :return: int
        """
        return len(self.children)

    def __iter__(self):
        """Returns a generator of the child nodes

        :return: generator
        """
        return iter(self.children)

    def __add__(self, other):
        """Adds the nodes from one compound to this one

        :param other: Compound
        """
        if isinstance(other, Compound):
            for child in other:
                self.addChild(child)

    def __sub__(self, other):
        if isinstance(other, Compound):
            for child in other:
                if child in self.children:
                    self.children.remove(child)

    def __contains__(self, item):
        return item in self.children

    def mutate(self):
        """Special method that allows this node to generate(mutate) other nodes as child nodes this can also contain
        other compounds
        """
        pass

    def child(self, name):
        for child in self:
            if child.name == name:
                return child
            elif child.isCompound():
                return child.child(name)

    def addChild(self, child):
        if child not in self.children:
            self.children.append(child)
            parent = child.parent
            if parent and parent.isCompound():
                parent.removeChild(child)
            child.parent = self
            return True
        return False

    def removeChild(self, child):
        if isinstance(child, str):
            child = self.child(child)
        if child.isLocked or child.isInternal:
            return False
        if child in self:
            child.disconnectAll()
            self.application.events.emitCallback(self.application.events.kNodeRemoved,
                                                 node=child)
            self.children.remove(child)
            return True
        return False

    def clear(self):
        for child in self.children:
            self.removeChild(child)
        self.children = []

    def remove(self):
        if self.isLocked or self.isInternal:
            return False
        par = self.parent
        if par is not None:
            self.clear()
            par.removeChild(self)
        return True

    def hasChild(self, name):
        for i in self:
            if i.name == name:
                return i

    def hasChildren(self):
        return len(self.children) > 0

    def topologicalOrder(self):
        return service.topologicalOrder(self.children)

    def serialize(self):
        data = super(Compound, self).serialize()
        data["children"] = [i.serialize() for i in self.children]
        return data