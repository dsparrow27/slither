"""A simple test for nested compound networks
"""
import contextlib
import pprint
import unittest

from slither import api
from slither.core import attribute
from slither.core import compound
from slither.plugins.nodes.math.basic import sum


class TestSubCompound(compound.Compound):
    input = attribute.AttributeDefinition(isInput=True, type_=float, default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_=float, default=0)

    def mutate(self):
        fourthNode = sum.Sum("fourthNodeSub", application=self.application)
        fourthNode.inputB = 20
        self.addChild(fourthNode)
        # connection between two attributes
        fourthNode.inputA = self.input
        # #todo compound output attributes need to support multiple connections
        # self.output = fourthNode.output


class TestCompound(compound.Compound):
    """Root compound node which contains other nodes, compounds do not expand until executed via the executor class
    """
    input = attribute.AttributeDefinition(isInput=True, type_=float, default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_=float, default=0)
    execution = attribute.AttributeDefinition(isOutput=True, type_=float, default=0)

    def mutate(self):
        firstNode = sum.Sum("firstNode", application=self.application)
        firstNode.inputA = 20
        firstNode.inputB = 10
        secondNode = sum.Sum("secondNode", application=self.application)
        secondNode.inputB = 10
        thirdNodeComp = TestSubCompound("thirdNodeComp", application=self.application)
        # add the nodes as children
        self.addChild(secondNode)
        self.addChild(thirdNodeComp)
        self.addChild(firstNode)
        self.execution = thirdNodeComp.output
        thirdNodeComp.input = secondNode.output
        secondNode.inputA = firstNode.output


def run():
    app = api.currentInstance
    app.root.addChild(TestCompound("subChild", application=app))
    app.execute(app.root, executorType=app.PARALLELEXECUTOR)
    return app


class TestGraphStandardExecutor(unittest.TestCase):
    @staticmethod
    @contextlib.contextmanager
    def executeGraphContext(app):
        try:
            app.root.addChild(TestCompound("subChild", application=app))
            app.execute(app.root, executorType=app.STANDARDEXECUTOR)
            yield
        finally:
            app.root.clear()

    def setUp(self):
        self.app = api.currentInstance

    def test_graphExecutesWithoutFail(self):
        with TestGraphStandardExecutor.executeGraphContext(self.app):
            pprint.pprint(self.app.root.serialize())

    def test_childCounts(self):
        with TestGraphStandardExecutor.executeGraphContext(self.app):
            self.assertEquals(len(self.app.root), 1)
            self.assertEquals(len(self.app.root.child("subChild")), 3)
            self.assertEquals(len(self.app.root.child("subChild").child("thirdNodeComp")), 1)

    def test_nodesProgress(self):
        def checkChildren(node):
            if node.isCompound():
                for c in iter(node):
                    checkChildren(c)
            self.assertEquals(node.progress, 100, msg="Failed progress state: {}".format(node))

        with TestGraphStandardExecutor.executeGraphContext(self.app):
            checkChildren(self.app.root)


if __name__ == "__main__":
    unittest.main()
