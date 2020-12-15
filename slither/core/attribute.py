import logging
import copy
from slither.core import errors

logger = logging.getLogger(__name__)


class NotSupportedAttributeIO(Exception):
    pass


class AttributeDefinition(object):
    """Acts as a blob of data to be attached to any given attribute, If you're
    """

    def __init__(self, type_=None, default=None, array=False, compound=False, doc="", **kwargs):
        self.name = kwargs.get("name", "")
        self.type = type_
        self.default = default
        self.array = array
        self.compound = compound
        self.required = kwargs.get("required", False)
        self.input = kwargs.get("input", False)
        self.output = kwargs.get("output", False)
        self.internal = kwargs.get("internal", False)

        doc += "\nType: {}".format(str(type_))

        self.__doc__ = doc
        self.validateDefault()
        if self.input and self.output:
            raise NotSupportedAttributeIO(self.name)
        value = kwargs.get("value")
        if value is not None:
            self.type.setValue(value)

    def __eq__(self, other):
        if not isinstance(other, AttributeDefinition):
            return False
        if self.name != other.name or self.type != other.type:
            return False
        if self.default != other.default or self.array != other.array:
            return False
        return True

    def setName(self, name):
        if name != self.name:
            self.name = name

    def documentation(self):
        """Returns the documentation for this definition.

        :rtype: str
        """
        return self.__doc__

    def validateDefault(self):
        """Validates the default value for this definition ensuring the correct datatype.
        """
        if self.array and not isinstance(self.default, list):
            self.default = list()

    def serialize(self, includeInternal=False):
        """Returns A dict representing this definition.

        :rtype: dict
        """
        attrValue = self.type.value()
        attrDefault = self.default
        if attrValue == attrDefault and (self.internal and not includeInternal):
            return {}
        return dict(name=self.name,
                    type_=self.type.typeName,
                    default=attrDefault,
                    array=self.array,
                    compound=self.compound,
                    required=self.required,
                    input=self.input,
                    output=self.output,
                    value=attrValue,
                    internal=self.internal,
                    doc=self.documentation())

    def deserialize(self, data):
        """Deserialize the provided data on this definition instance. The data must be
        in the same form as serialize()

        :param data: The data to apply to this instance
        :type data: dict
        """
        for name, value in iter(data.items()):
            if name == "value":
                self.type.setValue(value)

            elif name not in ("type",) and hasattr(self, name) and value != self.__getattribute__(name):
                # logger.debug("Setting Attribute {} parameter: {} -> {}".format(self, name, value))
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
        self._upstream = None
        self._value = self.definition.type
        self.id = 0

    @property
    def upstream(self):
        return self._upstream

    @upstream.setter
    def upstream(self, value):
        self._upstream = value
        if self.node is not None:
            self.node.setDirty(True)

    @property
    def isElement(self):
        return self.parent.isArray

    @property
    def isCompound(self):
        return self.definition.compound

    @property
    def isArray(self):
        return self.definition.array

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

    def __eq__(self, other):
        return self.node.id == other.node.id and self.id == other.id

    def __ne__(self, other):
        return self.node.id != other.node.id or self.id != other.id

    def name(self):
        return self.definition.name

    def setName(self, name):
        oldName = self.definition.name
        self.definition.setName(name)
        self.node.graph.application.events.emit(self.node.graph.application.events.attributeNameChanged,
                                                sender=self,
                                                attribute=self, oldName=oldName, name=name)

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
        if self._upstream is not None:
            return self._upstream.value()
        return self._value.value()

    def setValue(self, value):
        logger.debug("Setting Attribute '{}' value too : {}".format(self, value))
        valueSet = self._value.setValue(value)
        if valueSet and self.node is not None and self.isInput():
            self.node.setDirty(True)
        return valueSet

    def isInput(self):
        """Returns True if this attribute is an output attribute"""
        return self.definition.input

    def isOutput(self):
        """Returns True if this attribute is an input attribute"""
        return self.definition.output

    def hasUpstream(self):
        """Determines if the current attribute has a connection, an attribute can have only one connection if its an
        input.

        :return: bool
        """
        return self.upstream is not None

    isConnected = hasUpstream

    def canConnect(self, attribute):
        isCompound = attribute.node.isCompound() or self.node.isCompound()
        if attribute.parent == self.node:
            logger.debug("Attribute's is on the same Node")
            return False
        elif attribute.isInput() and self.isInput() and not isCompound:
            logger.debug("Attribute is an input and neither the node nor the attr.node is a compound")
            return False
        elif attribute.isOutput() and self.isOutput() and not isCompound:
            logger.debug("Attribute is an output and neither the node nor the attr.node is a compound")
            return False
        elif not attribute.type().supportsType(self.type()):
            logger.debug("Attribute types are not the same: {}".format(self.type().Type))
            return False
        logger.debug("Able to connect")
        return True

    def isConnectedTo(self, attribute):
        if self.isInput():
            upstream = self.upstream
            if upstream is not None and upstream == attribute:
                return True
        elif self.isOutput():
            return attribute.isConnectedTo(self)
        return True

    def connect(self, attr):
        if self == attr:
            raise errors.UnsupportedConnectionCombinationError(self, attr)
        attrNode = attr.node
        selfNode = self.node
        if attrNode == selfNode:
            raise errors.UnsupportedConnectionCombinationError(self, attr)
        src = self
        dest = attr
        attrParent = attrNode.parent
        selfParent = selfNode.parent
        if self.isInput() and attr.isOutput():
            src = attr
            dest = self
        # compound input attribute to child input
        elif self.isInput() and attr.isInput():
            # if we connecting from the child attr to the compound input
            if selfParent == attrNode:
                src = attr
                dest = self
        elif self.isOutput() and attr.isOutput():
            if attrParent == selfNode:
                src = attr
                dest = self
        self.node.createConnection(src, dest)

    def disconnect(self):
        if self.hasUpstream():
            self.upstream = None
            return True
        return False

    def serialize(self):

        data = self.definition.serialize()
        if data:
            data["id"] = self.id
        return data

    def deserialize(self, data):
        if self.definition:
            self.definition.deserialize(data)
            self.id = data.get("id", self.id)
            self.setValue(data.get("value"))


class CompoundAttribute(Attribute):
    type_ = "compound"

    def __init__(self, definition, node=None):
        self.children = []
        super(CompoundAttribute, self).__init__(definition, node=node)

    def __repr__(self):
        return "CompoundAttribute(%s)" % (self.name())

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

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
        definition = copy.deepcopy(self.definition)
        # data["array"] = data
        definition.name = self.name() + "[{}]".format(len(self) + 1)
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
