import os

from slither.core import types


def isIteratable(obj):
    try:
        for i in iter(obj):
            return True
    except TypeError:
        return False


class FloatType(types.DataType):
    Type = "kFloat"

    def __init__(self, value=None, default=None):
        super(FloatType, self).__init__(
            0.0 if value is None else value,
            0.0 if default is None else default
        )

    def __add__(self, other):
        return self.__class__(self._value + other.value())

    def __neg__(self, other):
        return self.__class__(self._value - other.value())

    def __float__(self):
        return float(self._value)

    def value(self):
        return float(self._value)

    def setValue(self, value):
        if self.value() != value:
            self._value = float(value)
            return True
        return False


class IntType(types.DataType):
    Type = "kInt"

    def __init__(self, value=None, default=None):
        super(IntType, self).__init__(
            0 if value is None else value,
            0 if default is None else default
        )

    def __add__(self, other):
        return self.__class__(self._value + other.value())

    def __neg__(self, other):
        return self.__class__(self._value - other.value())

    def __int__(self):
        return int(self._value)

    def value(self):
        return int(self)

    def setValue(self, value):
        if self.value() != value:
            self._value = int(value)
            return True
        return False


class StringType(types.DataType):
    Type = "kString"

    def __init__(self, value=None, default=None):
        super(StringType, self).__init__(
            "" if value is None else value,
            "" if default is None else default
        )

    def __str__(self):
        return str(self._value)

    def value(self):
        return str(self)

    def setValue(self, value):
        if self.value() != value:
            self._value = str(value)
            return True
        return False


class BooleanType(types.DataType):
    Type = "kBool"

    def __init__(self, value=None, default=None):
        super(BooleanType, self).__init__(
            False if value is None else value,
            False if default is None else default
        )

    def __nonzero__(self):
        return bool(self._value)

    def value(self):
        return bool(self)

    def setValue(self, value):
        if self.value() != value:
            self._value = bool(value)
            return True
        return False


class DictType(types.DataType):
    Type = "kDict"

    def __init__(self, value=None, default=None):
        super(DictType, self).__init__(
            {} if value is None else value,
            {} if default is None else default
        )

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
            return True
        return False


class FileType(StringType):
    Type = "kFile"

    def exists(self):
        return os.path.exists(self._value)


class DirectoryType(StringType):
    Type = "kDirectory"


class ListType(types.DataType):
    Type = "kList"

    def __init__(self, value=None, default=None):
        super(ListType, self).__init__(
            [] if value is None else value,
            [] if default is None else default
        )

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
            if not isIteratable(value):
                value = list(value)
            self._value = value
            return True
        return False


class MultiType(types.DataType):
    Type = "kMulti"
