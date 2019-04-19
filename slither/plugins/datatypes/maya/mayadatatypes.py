from maya.api import OpenMaya as om2

from slither import api


class MObjectHandle(api.DataType):
    Type = "kMObjectHandle"

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = om2.MObjectHandle(value)
