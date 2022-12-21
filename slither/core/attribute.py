import dataclasses

import copy
from slither.core import errors
from typing import Any
from zoo.core.util import zlogging

logger = zlogging.getLogger(__name__)


@dataclasses.dataclass
class AttributeDefinition:
    """Acts as a blob of data to be attached to any given attribute, If you're
    """
    name: str
    type: Any
    doc: str = ""
    array: bool = False
    compound: bool = False
    required: bool = False
    input: bool = False
    output: bool = False
    internal: bool = False
    min: float = -999999
    max: float = 999999
    serializable: bool = True
    exec: bool = False
    default: Any = None
    value: Any = None
    id: int = -1

    def __post_init__(self):
        self.doc += "\nType: {}".format(str(self.type))

        self.__doc__ = self.doc
        self.validateDefault()
        if self.input and self.output:
            raise errors.NotSupportedAttributeIOError(self.name)

        value = self.value or self.default
        if value is not None:
            self.type.setValue(value)


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
        if not self.serializable:
            return {}
        attrValue = self.type.value()
        attrDefault = self.default
        data = dict(name=self.name,
                    default=attrDefault,
                    value=attrValue)
        if not self.internal and not includeInternal:
            data.update(dict(
                type=self.type.typeName,
                array=self.array,
                compound=self.compound,
                required=self.required,
                input=self.input,
                output=self.output,
                internal=self.internal,
                doc=self.documentation()))
        return data

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
    """Base Attribute Class
    """
    type_ = "generic"

    def __init__(self, definition, node=None):
        """
        :param definition:
        :type definition: :class:`AttributeDefinition`
        :param node:
        :type node: :class:`slither.core.node.DependNode`
        """
        self.definition = definition
        # node that this attribute is attached too.
        self.node = node
        # parent attribute
        self.parent = None
        self._value = self.definition.type
        self._upstreamConnections = []  # type: list[Attribute]
        self._downstreamConnections = []  # type: list[Attribute]

    @property
    def isElement(self):
        """

        :return:
        :rtype: bool
        """
        return self.parent.isArray

    @property
    def isCompound(self):
        """

        :return:
        :rtype: bool
        """
        return self.definition.compound

    @property
    def isArray(self):
        """

        :return:
        :rtype: bool
        """
        return self.definition.array

    def __repr__(self):
        return "attribute(%s)" % (self.name())

    def __eq__(self, other):
        return self.node.name == other.node.name and self.name() == other.name()

    def __ne__(self, other):
        return self.node.name != other.node.name or self.name() != other.name()

    def name(self):
        """

        :return:
        :rtype: str
        """
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
        """

        :return:
        :rtype: :class:`slither.core.types.DataType`
        """
        return self.definition.type

    def value(self):
        if self.hasUpstream():
            if self.supportsMultipleConnections():
                return [upstream.value() for upstream in self._upstreamConnections]
            for upstream in self._upstreamConnections:
                return upstream.value()
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

    def upstream(self):
        """
        :return:
        :rtype: list[:class:`Attribute`]
        """
        return self._upstreamConnections

    def downstream(self):
        return self._downstreamConnections

    def supportsMultipleConnections(self):
        return False

    def hasUpstream(self):
        """Determines if the current attribute has a connection, an attribute can have only one connection if its an
        input.

        :return: bool
        """
        return len(self._upstreamConnections) != 0

    isConnected = hasUpstream

    @staticmethod
    def canConnect(source, destination):
        """

        :param source:
        :type source: :class:`Attribute`
        :param destination:
        :type destination: :class:`Attribute`
        :return:
        :rtype: bool
        """
        isCompound = destination.node.isCompound() or source.node.isCompound()

        if source == destination:
            logger.debug("Source and Destination attributes are the same")
            # print("source is the same", source, destination)
            return False
        if destination.parent == source.node:
            logger.debug("Attribute's is on the same Node")
            # print("Attribute's is on the same Node")
            return False
        elif destination.isInput() and source.isInput() and not isCompound:
            logger.debug("Attribute is an input and neither the node nor the attr.node is a compound")
            # print("Attribute is an input and neither the node nor the attr.node is a compound")
            return False
        elif destination.isOutput() and source.isOutput() and not isCompound:
            logger.debug("Attribute is an output and neither the node nor the attr.node is a compound")
            # print("Attribute is an output and neither the node nor the attr.node is a compound")
            return False
        elif not destination.type().supportsType(source.type()):
            logger.debug("Attribute types are not the same: {}".format(source.type().Type))
            # print("Attribute types are not the same: {}".format(source.type().Type))
            return False
        elif destination.hasUpstream() and not destination.supportsMultipleConnections():
            # print("already contains upsteam")
            return False
        elif source.isConnectedTo(destination):
            # print(source, destination, "already connected")
            return False

        logger.debug("Able to connect")
        return True

    def isConnectedTo(self, attribute):
        if self.isInput():
            for upstream in self._upstreamConnections:
                if upstream == attribute:
                    return True
        elif self.isOutput():
            for attr in self._downstreamConnections:
                if attr == attribute:
                    return True
        return False

    def connect(self, attr):
        """

        :param attr:
        :type attr: :class:`Attribute`
        :return:
        :rtype:
        """
        src, dest = self._returnCorrectSourceDestination(self, attr)
        if not self.canConnect(src, dest):
            raise errors.UnsupportedConnectionCombinationError(self, attr)
        logger.debug("Creating connection between: {}->{}".format(src.fullName(), dest.fullName()))

        if not dest.supportsMultipleConnections():
            dest.disconnect()
        dest._upstreamConnections.append(src)
        if dest.node is not None:
            dest.node.setDirty(True)

        src._downstreamConnections.append(dest)
        self.node.graph.createConnection(src, dest)
        connection = {"source": src.node, "destination": dest.node,
                      "input": dest, "output": src}

        app = self.node.graph.application
        self.node.graph.connections.append(connection)
        app.events.emit(app.events.connectionsCreated,
                        sender=self,
                        connections=[dict(sourcePlug=src, destinationPlug=dest)]
                        )

    def disconnect(self, attribute=None):
        # if self.isOutput():
        #     return self.disconnectDestination(attribute)
        # if self.isOutput():
        #     raise ValueError("Attribute must not be a Output: {}".format(self))
        if attribute is None:
            upstreamConnections = self.upstream()
            self._upstreamConnections = []
            for upstream in upstreamConnections:
                upstream.disconnectDestination(self)
            return True
        upstreamConnections = self.upstream()
        _upstreamConnections = []
        for upstream in upstreamConnections:
            if upstream != attribute:
                _upstreamConnections.append(upstream)
            else:
                upstream.disconnectDestination(self)
        self._upstreamConnections = _upstreamConnections
        # connection = {"source": src.node, "destination": dest.node,
        #               "input": dest, "output": src}
        #
        # app = self.node.graph.application
        # self.node.graph.connections.append(connection)
        # app.events.emit(app.events.connectionsCreated,
        #                 sender=self,
        #                 connections=[dict(sourcePlug=src, destinationPlug=dest) for ]
        #                 )
        return False

    def disconnectDestination(self, attribute):
        """

        :param attribute: the downstream attribute to disconnect from
        :type attribute: :class:`Attribute`
        :return:
        :rtype: bool
        """
        if attribute.hasUpstream() is not None:
            attribute.disconnect()
        connections = [attr for attr in self._downstreamConnections if attr != attribute]
        self._downstreamConnections = connections
        return True

    def serialize(self):
        return self.definition.serialize()

    def deserialize(self, data):
        if self.definition:
            self.definition.deserialize(data)
            self.setValue(data.get("value"))

    def delete(self):
        self.disconnect()
        for downstream in self.downstream():
            self.disconnectDestination(downstream)

    @staticmethod
    def _returnCorrectSourceDestination(src, dest):
        """Internal Method to correctly return the right source and destination.

        This is used in situations where the user can pass the source and destination
        in different orders. ie. src.connect(dest)  vs dest.connect(src). Both a valid
        but internal logic requires  source -> destination

        :param src:
        :type src: :class:`Attribute`
        :param dest:
        :type dest: :class:`Attribute`
        :return:
        :rtype: tuple(:class:`Attribute`, :class:`Attribute`)
        """
        attrNode = dest.node
        selfNode = src.node
        source = src
        destination = dest
        selfParent = selfNode.parent
        if src.isInput() and dest.isOutput():
            source = dest
            destination = src
        # compound input attribute to child input
        elif src.isInput() and dest.isInput():
            # if we connecting from the child attr to the compound input
            if selfParent == attrNode:
                source = dest
                destination = src
        elif src.isOutput() and dest.isOutput():
            attrParent = attrNode.parent
            if attrParent == selfNode:
                source = dest
                destination = src
        # print(src, dest)
        return source, destination


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

    def connect(self, attr):
        if not attr.definition.compound:
            raise errors.AttributeCompatiblityError(self, attr)
        return super(CompoundAttribute, self).connect(attr)

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
        if self._upstreamConnections:
            if self.supportsMultipleConnections():
                return [upstream.value() for upstream in self._upstreamConnections]
            return self._upstreamConnections[0].value()
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
        definition.array = False
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

    def connect(self, attr):
        if not attr.definition.array:
            raise errors.AttributeCompatiblityError(self, attr)
        return super(ArrayAttribute, self).connect(attr)


class ExecAttribute(Attribute):
    type_ = "exec"

    def value(self):
        return

    def setValue(self, value):
        return

    def supportsMultipleConnections(self):
        return True
