"""A simple test for nested compound networks
"""
import pprint

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
    app.execute(app.root.child("subChild"), executorType=app.PARALLELEXECUTOR)
    return app


if __name__ == "__main__":
    app = run()
    pprint.pprint(app.root.serialize())
