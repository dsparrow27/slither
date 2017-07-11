import copy

from slither.core import attribute
from slither.core import service


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
    """
    """
    __metaclass__ = NodeMeta
    category = ""
    tags = set()
    documentation = ""

    def __init__(self, name):
        self.name = name
        self.parent = None
        self.attributes = []
        self.progress = 0
        self.metadata = {}
        self.dependencies = []  # node level dependencies

        for name, attrDef in iter(self.__class__.__dict__.items()):
            if isinstance(attrDef, attribute.AttributeDefinition):
                attr = service.createAttribute(self, attrDef)
                self.addAttribute(attr)

    def execute(self):
        pass

    @staticmethod
    def isCompound():
        """StaticMethod, Returns whether or not this node is a compound.
        :return: True if a compound.
        :rtype: bool
        """
        return False

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.name)

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

    def addDependency(self, node):
        if node not in self.dependencies:
            self.dependencies.append(node)

    @classmethod
    def type(cls):
        """Returns the type of this node
        :rtype: string
        """
        return cls.__class__.__name__

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

    def attribute(self, name):
        for attr in self.iterAttributes():
            if attr.name() == name:
                return attr

    def addAttribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes.append(attribute)
            return True
        return False

    def createAttribute(self, name, **kwargs):
        if not kwargs.get("input"):
            definition = attribute.OutputDefinition(**kwargs)
        else:
            definition = attribute.InputDefinition(**kwargs)
        definition.name = name
        attr = service.createAttribute(self, definition)
        name = attr.name()

        className = "_%s" % name if not name.startswith("_") else name
        super(BaseNode, self).__setattr__(className, definition)
        self.addAttribute(attr)
        return attr

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
        return [i for i in self.iterInputs()]

    def attributeCount(self):
        return len(self.attributes)

    def iterAttributes(self):
        return iter(self.attributes)

    def outputs(self):
        return [i for i in self.iterOutputs()]

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
