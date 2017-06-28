from slither.utils import generic
from slither.core import types


class FloatType(types.DataType):
    Type = float

    def value(self):
        return float(self._value)

    def setValue(self, value):
        if self.value() != value:
            self._value = float(value)


class IntType(types.DataType):
    Type = int

    def value(self):
        return int(self._value)

    def setValue(self, value):
        if self.value() != value:
            self._value = int(value)


class StringType(types.DataType):
    Type = str

    def value(self):
        return str(self._value)

    def setValue(self, value):
        if self.value() != value:
            self._value = str(value)


class BooleanType(types.DataType):
    Type = bool

    def value(self):
        return bool(self._value)

    def setValue(self, value):
        if self.value() != value:
            self._value = bool(value)


class DictType(types.DataType):
    Type = dict

    def __init__(self, value):
        super(DictType, self).__init__(value)
        self._value = dict()

    def __setattr__(self, key, value):
        if hasattr(self, "_value") and key in self._value:
            self._value[key]["value"] = value
            return
        super(DictType, self).__setattr__(key, value)

    def __getattr__(self, key):
        if hasattr(self, "_value"):
            if key in self._value and key != "Type":
                return self._value[key]["value"]
        return super(DictType, self).__getattribute__(key)

    def setValue(self, value):
        if value != self.value():
            self._value = dict(value)


class ListType(types.DataType):
    Type = list

    def __iter__(self):
        return iter(self._value)

    def __len__(self):
        return len(self._value)

    def __setitem__(self, key, value):
        self._value[key] = value

    def __getitem__(self, index):
        return self._value[index]

    def setValue(self, value):
        if self.value() != value:
            if not generic.isIteratable(value):
                value = list(value)
            self._value = value
