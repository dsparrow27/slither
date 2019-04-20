import logging

logger = logging.getLogger(__name__)


class DataType(object):
    Type = None

    def __init__(self, value=None, default=None):
        self._value = value
        self.default = default

    @property
    def typeName(self):
        if self.Type is None:
            return None
        elif isinstance(self.Type, basestring):
            return self.Type
        return self.Type.__name__

    def __eq__(self, other):
        return self.Type == other.Type and self._value == other.value

    def __ne__(self, other):
        return self.Type != other.Type or self._value != other.value()

    def value(self):
        return self._value

    def setValue(self, value):
        if self._value != value:
            self._value = value
            return True
        return False

    def serialize(self):
        return self._value
