import logging
from zoovendor import six

logger = logging.getLogger(__name__)


class DataType(object):
    Type = None

    def supportsType(self, type_):
        return self.Type == type_.Type

    @classmethod
    def create(cls, info):
        newCls = cls(info.get("value"), info.get("default"))
        return newCls

    def __init__(self, value=None, default=None):
        self.__dict__["_value"] = value
        self.__dict__["default"] = default

    @property
    def typeName(self):
        if self.Type is None:
            return None
        elif isinstance(self.Type, six.string_types):
            return self.Type
        return self.Type.__name__

    def __eq__(self, other):
        return self.Type == other.Type and self._value == other.value

    def __ne__(self, other):
        return self.Type != other.Type or self._value != other.value()

    def __repr__(self):
        return "<{}>value: {}, default: {}".format(self.__class__.__name__, self._value, self.default)

    def value(self):
        return self._value

    def setValue(self, value):
        if self._value != value:
            self._value = value
            return True
        return False

    def serialize(self):
        return self._value
