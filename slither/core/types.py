import logging


logger = logging.getLogger(__name__)


class DataType(object):
    Type = None

    def __init__(self, value=None):
        self._value = value

    def __eq__(self, other):
        return self.Type == other.Type and self._value == other.value

    def __ne__(self, other):
        return self.Type != other.Type or self._value != other.value()

    def value(self):
        return self._value

    def setValue(self, value):
        if self._value != value:
            self._value = value