import logging

from slither.core import errors

logger = logging.getLogger("Slither")


class AttributeDefinition(object):
    """Acts as a blob of data to be attached to any given attribute, If you're
    """

    def __init__(self, type_=None, default=None, array=False, compound=False, doc="", **kwargs):
        self.name = kwargs.get("name", "")
        self.type = type_
        self.default = default
        self.isArray = array
        self.isCompound = compound
        self.required = kwargs.get("required", False)
        self.affectedBy = []
        self.isInput = kwargs.get("isInput", False)
        self.isOutput = kwargs.get("isOutput", False)

        doc += "\nType: {}".format(str(type_))

        self.__doc__ = doc
        self.validateDefault()
        self._validateType()

    def _validateType(self):
        """Validate's the dataType and converts it if necessary.
        """
        self.type = self.type(self.default)

    def __eq__(self, other):
        if not isinstance(other, AttributeDefinition):
            return False
        if self.name != other.name or self.type != other.type:
            return False
        if self.default != other.default or self.isArray != other.isArray:
            return False
        return True

    def setName(self, name):
        if name != self.name:
            self.name = name

    def documentation(self):
        return self.__doc__

    def match(self, definition):
        self.__dict__ = definition.__dict__

    def validateDefault(self):
        if self.isArray and not isinstance(self.default, list):
            self.default = list()

    def serialize(self):
        return dict(name=self.name,
                    type=self.type.typeName,
                    default=self.default,
                    isArray=self.isArray,
                    isCompound=self.isCompound,
                    required=self.required,
                    affectedBy=[i.name for i in self.affectedBy],
                    isInput=self.isInput,
                    isOutput=self.isOutput,
                    value=self.type.value())

    def deserialize(self, data):
        for name, value in iter(data.items()):
            if name in ("type", "affectedBy") and value != self.__getattribute__(name):
                self.__setattr__(name, value)


class Attribute(object):
    type_ = "generic"

    def __init__(self, definition, node=None):
        """
        :param definition:
        :param node:
        """
        self.definition = definition
        # node that this attribute is attached too.
        self.node = node
        # parent attribute
        self.parent = None
        self.upstream = None
        self._value = None
        if definition:
            self._value = self.definition.type

    @property
    def isElement(self):
        return self.parent.definition.isArray

    @property
    def isCompound(self):
        return self.definition.isCompound

    @property
    def isArray(self):
        return self.definition.isArray

    def __repr__(self):
        return "attribute(%s)" % (self.name())

    def __float__(self):
        try:
            return float(self.value())
        except TypeError:
            pass

    def __int__(self):
        try:
            return int(self.value())
        except TypeError:
            pass

    def name(self):
        return self.definition.name

    def setName(self, name):
        self.definition.setName(name)

    def fullName(self):
        if self.parent is not None:
            return "|".join([self.parent.fullName(), self.name()])
        prefix = ""
        if self.node is not None:
            prefix = self.node.fullName()

        return "|".join([prefix, self.name()])

    def setParent(self, parent):
        if self.parent != parent:
            self.parent = parent
            logger.debug("Parent for child: {} has been set to: {}".format(self.fullName(),
                                                                           self.parent.fullName()))

    def setNode(self, node):
        if self.node != node:
            self.node = node
            logger.debug("Parent for child: {} has been set to: {}".format(self.fullName(),
                                                                           self.node.fullName()))

    def type(self):
        return self.definition.type

    def value(self):
        if self.upstream is not None:
            return self.upstream.value()
        return self._value.value()

    def setValue(self, value):
        return self._value.setValue(value)

    def isInput(self):
        """Returns True if this attribute is an output attribute"""
        return self.definition.isInput

    def isOutput(self):
        """Returns True if this attribute is an input attribute"""
        return self.definition.isOutput

    def hasUpstream(self):
        """Determines if the current attribute has a connection, an attribute can have only one connection if its an
        input.

        :return: bool
        """
        return self.upstream is not None

    def canConnect(self, attribute):
        isCompound = attribute.node.isCompound() or self.node.isCompound()
        if attribute.parent == self.node:
            return False
        elif attribute.isInput() and self.isInput() and not isCompound:
            return False
        elif attribute.isOutput() and self.isOutput() and not isCompound:
            return False
        elif attribute.type().Type != self.type().Type:
            return False

        return True

    def isConnectedTo(self, attribute):
        if self.isInput():
            upstream = self.upstream
            if upstream is not None and upstream == attribute:
                return True
        elif self.isOutput():
            return attribute.isConnectedTo(self)
        return True

    def connectUpstream(self, attribute):
        if self.upstream is not None:
            raise errors.AttributeAlreadyConnected(self, attribute)
        self.upstream = attribute
        logger.debug("Connected Attributes, upstream: {}, downstream: {}".format(self.upstream.fullName(),
                                                                                 self.fullName()))

    def connectDownstream(self, attribute):
        attribute.connectUpstream(self)

    def disconnect(self):
        if self.hasUpstream():
            self.upstream = None

    def serialize(self):
        data = {"name": self.fullName()
                }
        definition = self.definition.serialize()
        data["value"] = self.value()
        data["definition"] = definition
        if self.node:
            data["parent"] = self.node.fullName()
        if self.upstream is not None:
            data["upstream"] = self.upstream.fullName()
        return data

    def deserialize(self, data):
        if self.definition:
            self.definition.deserialize(data["definition"])
            self.setValue(data.get("value"))


class CompoundAttribute(Attribute):
    type_ = "compound"

    def __init__(self, definition, node=None):
        super(CompoundAttribute, self).__init__(definition, node=node)
        self.children = []

    def __repr__(self):
        return "CompoundAttribute(%s)" % (self.name())

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __setattr__(self, key, value):
        if key != "children":
            attr = getattr(self, key)
            if attr:
                attr.setValue(value)

    def __getattr__(self, name):
        for child in self.children:
            if child.name() == name:
                return name
        return super(CompoundAttribute, self).__getattribute__(name)

    def addChild(self, child):
        if child not in self.children:
            self.children.append(child)
            child.setParent(self)

    def removeChild(self, child):
        if child not in self.children:
            self.children.remove(child)
            child.setParent(None)

    def serialize(self):
        data = super(CompoundAttribute, self).serialize()
        data["children"] = [i.serialize() for i in self]
        return data


class ArrayAttribute(Attribute):
    """Array base Attribute which is used for sequence data types eg.lists, tuples etc
    """
    type_ = "array"

    def __init__(self, definition, node=None):
        super(ArrayAttribute, self).__init__(definition, node)
        self.elements = []

    def __repr__(self):
        return "ArrayAttribute(%s)" % (self.name())

    def __getitem__(self, item):
        if item in range(len(self)):
            return self.elements[item]

    def __setitem__(self, key, value):
        self.elements[key].setValue(value)

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def clear(self):
        for element in self.elements:
            element.disconnect()
        self.elements = []

    def value(self):
        """override
        :return:
        """
        if self.upstream is not None:
            value = self.upstream.value()
            if not isinstance(value, list):
                return [value]
            return value
        return [element.value() for element in self.elements]

    def setValue(self, value):
        self.clear()
        for i in value:
            self.append(i)

    def element(self, index):
        if index in range(len(self)):
            return self.elements[index]

    def append(self, value):
        data = self.definition.serialize()
        data["array"] = data
        data["name"] = self.name() + "[{}]".format(len(self) + 1)
        definition = AttributeDefinition(**data)
        attr = Attribute(definition, node=self)
        attr.setValue(value)
        self.elements.append(attr)
        return self

    def remove(self, index):
        self.pop(index)

    def insert(self, value, index):
        self.elements.insert(index, value)

    def pop(self, index):
        if index in range(len(self)):
            attr = self.elements.pop(index)
            attr.disconnect()
            return attr
