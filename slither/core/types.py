import logging


logger = logging.getLogger(__name__)


class DataType(object):
    Type = ""

    def __init__(self, value=None):
        self._value = value

    def __eq__(self, other):
        return isinstance(other, DataType) and self._value == other.value

    def value(self):
        return self._value

    def setValue(self, value):
        if self._value != value:
            self._value = value

