from slither.core import types


class MObjectHandle(types.DataType):
    Type = "MObjectHandle"

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value