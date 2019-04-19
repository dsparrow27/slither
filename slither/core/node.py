import copy
import logging

from slither.core import attribute
from slither.core import service
from slither.core import types

logger = logging.getLogger(__name__)


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
    Type = ""
    category = ""
    tags = set()
    documentation = ""

    def __init__(self, name, application):
        self.application = application
        self.name = name

        self.metadata = {}
        self.isLocked = False
        self.isInternal = False
        self._selected = False
        self._parent = None
        self.initialize()

    def initialize(self):
        pass

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected != value:
            self._selected = value

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

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if self._parent != node:
            self._parent = node

    def depth(self):
        index = 0
        if self.parent:
            index += self.parent.depth + 1
        return index

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

    def type(self):
        """Returns the type of this node
        :rtype: string
        """
        return self.Type

    def setName(self, name):
        """Sets the name of the node if the name already exists in the graph then a number will be append
        :param name: The name of the node.
        :type name: str
        :rtype: str
        """
        if self.name != name:
            self.name = name

        return self.name

    def fullName(self):
        """Returns the full path name of the node eg. |parent|currentNode
        :rtype str
        """
        if self.parent:
            return "|".join([self.parent.fullName(), self.name])
        return self.name

    def serialize(self):
        data = {"name": self.name,
                "parent": self.parent.fullName() if self.parent else None,
                "isCompound": self.isCompound(),
                "type": self.Type
                }
        return data

    def deserialize(self, data):
        pass


class DependencyNode(BaseNode):
    __metaclass__ = NodeMeta

    def __init__(self, name, application):
        super(DependencyNode, self).__init__(name, application)
        self.attributes = []
        attrDef = attribute.AttributeDefinition(isInput=True,
                                                isOutput=True,
                                                type_=types.list,
                                                default=list(),
                                                required=False, array=True,
                                                doc="Node Level dependencies")
        attrDef.name = "Dependencies"
        self.createAttribute(attrDef)

        for name, attrDef in iter(self.__class__.__dict__.items()):
            if isinstance(attrDef, attribute.AttributeDefinition):
                self.createAttribute(copy.deepcopy(attrDef))

    def __setattr__(self, name, value):
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

    def attribute(self, name):
        for attr in self.iterAttributes():
            if attr.name() == name:
                return attr

    def addAttribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes.append(attribute)
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

    def disconnectAll(self):
        for attr in self.iterAttributes():
            attr.disconnect()

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

    def serialize(self):
        data = super(DependencyNode, self).serialize()
        data["attributes"] = [i.serialize() for i in self.attributes],
        return data

    def deserialize(self, data):
        super(DependencyNode, self).deserialize(data)
        for attr in data["attributes"]:
            currentAttr = self.attribute(attr["name"].split("|")[-1])
            if currentAttr is not None:
                currentAttr.deserialize(attr)


class Comment(BaseNode):
    Type = "comment"


class Pin(DependencyNode):
    Type = "pin"


class ComputeNode(DependencyNode):
    """Node which has a computation operation
    """

    def __init__(self, name, application):
        super(ComputeNode, self).__init__(name, application)
        self._progress = 0
        self._dirty = False

    def process(self):
        try:
            self.validate()
            self.progress = 0
            self.execute()
            self.progress = 100
        except Exception:
            self.progress = 0
            raise

    def validate(self):
        return True

    def execute(self):
        pass

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value

    def dirty(self):
        return self._dirty

    def setDirty(self, state, propagate=True):
        if self._dirty == state:
            return
        self._dirty = state
        # if we setting to a dirty state and we need to propagate
        # then loop the downstream nodes and set their state
        if state and propagate:
            for dependent in self.downStreamNodes():
                dependent.setDirty(state, propagate)


class Compound(ComputeNode):
    """The Compound class encapsulates a set of child nodes, which can include other compounds.
    We provide methods to query the children nodes of the current compound.
    """
    Type = "Compound"

    def __init__(self, name, application):
        """
        :param name: The name that this node will have, if the name already exist a number we be appended.
        :type name: str
        """
        super(Compound, self).__init__(name, application=application)
        self.children = []

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

    def createNode(self, name, type_):
        exists = self.child(name)
        if exists:
            newName = name
            counter = 1
            while self.child(newName):
                newName = name + str(counter)
                counter += 1
            name = newName
        newNode = self.application.nodeRegistry.loadPlugin(type_, name=name, application=self)
        if newNode is not None:
            self.addChild(newNode)
            # should emit a event
            return newNode

    def removeChild(self, child):
        if isinstance(child, str):
            child = self.child(child)
        if child.isLocked or child.isInternal:
            return False
        if child in self:
            child.disconnectAll()
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

    def deserialize(self, data):
        super(Compound, self).deserialize(data)
        for child in data.get("children", []):
            newNode = self.createNode(child["name"], type_=child["type"])
            if newNode is None:
                raise ValueError("Failed to create node: {}".format(child["name"]))
            newNode.deserialize(child)
