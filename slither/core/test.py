import unittest
import os
import tempfile
from slither.core import nodeRegistry
from slither.core import executor


class BaseUnitest(unittest.TestCase):
    """This Class acts as the base for all unitests, supplies a helper method for creating tempfile which
    will be cleaned up once the class has been shutdown.
    If you override the tearDownClass method you must call super or at least clean up the _createFiles set
    """
    _createdFiles = set()

    @classmethod
    def createTemp(cls, suffix, prefix=None, dir=None):
        """Create's a temp file and stores it on the class
        :param suffix: str, the files name suffix
        :return: str, the temp file path
        """
        temp = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
        cls._createdFiles.add(temp)
        return temp

    @classmethod
    def tearDownClass(cls):
        """Cleans up all the temp files that have been created.
        """
        super(BaseUnitest, cls).tearDownClass()
        for i in cls._createdFiles:
            if os.path.exists(i):
                if os.path.isdir(i):
                    os.rmdir(i)
                else:
                    os.remove(i)
        cls._createdFiles.clear()


class TestExecutor(BaseUnitest):
    registry = nodeRegistry.NodeRegistry()

    def registerTasks(self, modulePath):
        for path in modulePath.split(os.pathsep):
            self.registry.registerByPackage(path)

    def createNode(self, type_, name):
        return self.registry.node(type_, name)

    def execute(self, node):
        executor.execute(node)
