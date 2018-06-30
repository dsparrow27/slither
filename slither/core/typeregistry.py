import inspect
import os

from slither.core import modules
from slither.core import types
from slither.core import classtypes


class DataTypeRegistry(object):
    __metaclass__ = classtypes.Singleton
    dataTypes = {types.DataType.Type: types.DataType}
    TYPE_LIB_ENV = "SLITHER_TYPE_LIB"

    def __init__(self):
        self.registerFromEnv(DataTypeRegistry.TYPE_LIB_ENV)

    @classmethod
    def dataType(cls, type_):
        if isinstance(type_, types.DataType):
            return type_
        if type_ in cls.dataTypes:
            return cls.dataTypes[type_]

    @classmethod
    def registerDataType(cls, classObject):
        name = classObject.Type
        if name not in cls.dataTypes:
            cls.dataTypes[name] = classObject

    @classmethod
    def registerFromEnv(cls, env):
        paths = os.environ.get(env)
        if not paths:
            raise ValueError("Cannot find environmentVariable -> %s" % env)
        for p in paths.split(os.pathsep):
            importedModule = None
            if p and os.path.isfile(p):
                importedModule = modules.importModule(p)
            if importedModule:
                cls.registerByModule(importedModule)
                continue

            cls.registerByPackage(p)

    @classmethod
    def registerByModule(cls, module):
        if inspect.ismodule(module):
            for member in modules.iterMembers(module, predicate=inspect.isclass):
                cls.registerDataType(member[1])

    @classmethod
    def registerByPackage(cls, pkg):
        visited = set()
        for subModule in modules.iterModules(pkg):
            filename = os.path.splitext(os.path.basename(subModule))[0]
            if filename.startswith("__") or filename in visited:
                continue
            visited.add(filename)
            subModuleObj = modules.importModule(subModule)
            if subModuleObj:
                cls.registerByModule(subModuleObj)
