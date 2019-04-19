from slither.core import types


class ShotgunType(types.DataType):
    Type = "kShotgun"

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value


class SgtkEngineType(types.DataType):
    Type = "ksgtkEngine"

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = value
