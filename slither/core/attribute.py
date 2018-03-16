from slither.core import typeregistry


class AttributeDefinition(object):
    """Acts as a blob of data to be attached to any given attribute, If you're
    """

    def __init__(self, type_=None, default=None, array=False, compound=False, doc=""):
        self.name = ""
        self.type = type_
        self.default = default
        self.isArray = array
        self.isCompound = compound
        self.__doc__ = doc
        self.validateDefault()
        self._validateType()

    def _validateType(self):
        """Validate's the dataType and converts it if necessary.
        """
        Type = typeregistry.DataTypeRegistry().dataType(self.type)
        if Type is None:
            raise TypeError("The request type -> %s is incorrect" % self.type)
        self.type = Type(self.default)

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
        return self.__dict__

    def deserialize(self, data):
        for name, value in iter(data.items()):
            if value != self.__getattribute__(name):
                self.__setattr__(name, value)


class InputDefinition(AttributeDefinition):
    """
    """

    def __init__(self, type_, default=None, required=False, array=False, doc=""):
        """
        """
        super(InputDefinition, self).__init__(type_, default, array=array, doc=doc)
        self.required = required


class OutputDefinition(AttributeDefinition):
    """
    """

    def __init__(self, type_, default=None, array=False, affectedBy=None, doc=""):
        """
        """
        super(OutputDefinition, self).__init__(type_, default, array=array, doc=doc)
        if affectedBy is None:
            affectedBy = []
        self.affectedBy = affectedBy


class Attribute(object):
    """
    """
    type_ = "generic"

    def __init__(self, definition, parent=None):
        """
        :param definition:
        :param parent:
        """
        self.definition = definition
        self.parent = parent
        self.upstream = None
        self._value = None
        if definition:
            self._value = self.definition.type

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

        self.parent.application.events.atttributeNameChanged.send(self, name)

    def fullName(self):
        if self.parent:
            return "|".join([self.parent.fullName(), self.name()])
        return self.name()

    def setParent(self, parent):
        if self.parent != parent:
            self.parent = parent

    def type(self):
        return self.definition.type

    def value(self):
        if self.upstream:
            return self.upstream.value()
        return self._value.value()

    def setValue(self, value):
        if self._value != value:
            self._value.setValue(value)
            self.parent.application.events.attributeValueChanged.send(self, value)

    def isInput(self):
        """Returns True if this attribute is an output attribute"""
        return isinstance(self.definition, InputDefinition)

    def isOutput(self):
        """Returns True if this attribute is an input attribute"""
        return isinstance(self.definition, OutputDefinition)

    def hasUpstream(self):
        """Determines if the current attribute has a connection, an attribute can have only one connection
        :return: bool
        """
        if self.upstream:
            return True
        return False

    def canConnect(self, attribute):
        if attribute.parent == self.parent:
            return False
        elif attribute.isInput() and self.isInput():
            return False
        elif attribute.isOutput() and self.isOutput():
            return False
        elif attribute.type() != self.type():
            return False

        return True

    def isConnectedTo(self, attribute):
        if self.isInput():
            upstream = self.upstream
            if upstream and upstream == attribute:
                return False
        elif self.isOutput():
            return attribute.isConnectedTo(self)
        return True

    def connectUpstream(self, attribute):
        if attribute != self.upstream:
            self.upstream = attribute
            self.parent.application.events.connectionAdded.send(attribute, self)
            return True
        return False

    def connectDownstream(self, attribute):
        attribute.connectUpstream(self)

    def disconnect(self):
        if self.hasUpstream():
            self.parent.application.events.connectionRemoved.send(self.upstream, self)
            self.upstream = None


    def serialize(self):
        data = {"name": self.fullName()
                }
        definition = self.definition.serialize()
        value = self.value()
        if definition:
            data["definition"] = definition
        if self.parent:
            data["parent"] = self.parent.fullName()
        data["value"] = value
        if self.upstream:
            data["upstream"] = self.upstream.fullName()
        return data

    def deserialize(self, data):
        if self.definition:
            self.definition.deserialize(data["attributeDefinition"])


class CompoundAttribute(Attribute):
    type_ = "compound"

    def __init__(self, definition, parent=None):
        super(CompoundAttribute, self).__init__(definition, parent=parent)
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

    def __init__(self, definition, parent=None):
        super(ArrayAttribute, self).__init__(definition, parent)

    def __repr__(self):
        return "ArrayAttribute(%s)" % (self.name())

    def __getitem__(self, item):
        if item in range(self):
            return self.value()[item]

    def __setitem__(self, key, value):
        self.value()[key] = value

    def __add__(self, other):
        if isinstance(other, Attribute):
            self.setValue(self.value() + other.value())
        elif isinstance(other, list):
            self.setValue(self.value() + other)
        else:
            self.setValue(self.value() + [other])

    def __iter__(self):
        return iter(self.value())

    def __len__(self):
        return len(self.value())

    def value(self):
        """override
        :return:
        """
        if self.upstream:
            value = self.upstream.value()
            if not isinstance(value, list):
                return [value]
            return self.upstream.value()
        return self._value

    def element(self, index):
        if index in range(self):
            return self.value()[index]

    def additem(self, value):
        self + value
        return self

    def remove(self, index):
        if index in range(self):
            value = self.value()
            value.remove(index)
            self.setValue(value)

    def insert(self, value, index):
        newvalue = self.value()
        newvalue.insert(index, value)
        self.setValue(newvalue)

    def pop(self, index):
        if index in range(self):
            value = self.value()
            popped = value.pop(index)
            return popped
