"""A simple test for nested compound networks
"""
import pprint


from slither.core import attribute
from slither.core import compound
from slither.core import executor
from slither.plugins.nodes.math.basic import sum


class TestSubCompound(compound.Compound):
    """
    """
    input = attribute.InputDefinition(type_=float, default=0)
    output = attribute.OutputDefinition(type_=float, default=0)

    def mutate(self):
        fourthNode = sum.Sum("fourthNodeSub")
        fourthNode.inputB = 20
        self.addChild(fourthNode)
        # connection between two attributes
        self.output = fourthNode.output
        fourthNode.inputA = self.input


class TestCompound(compound.Compound):
    """Root compound node which contains other nodes, compounds do not expand until executed via the executor class
    """
    input = attribute.InputDefinition(type_=float, default=0)
    output = attribute.OutputDefinition(type_=float, default=0)
    execution = attribute.OutputDefinition(type_=float, default=0)

    def mutate(self):
        firstNode = sum.Sum("firstNode")
        firstNode.inputA = 20
        firstNode.inputB = 10
        secondNode = sum.Sum("secondNode")
        secondNode.inputB = 10
        thirdNodeComp = TestSubCompound("thirdNodeComp")
        #add the nodes as children
        self.addChild(secondNode)
        self.addChild(thirdNodeComp)
        self.addChild(firstNode)
        self.execution = thirdNodeComp.output
        thirdNodeComp.input = secondNode.output
        secondNode.inputA = firstNode.output


if __name__ == '__main__':
    import os
    from slither.core import nodeRegistry
    from slither.core import typeregistry

    NODE_LIB_ENV = "SLITHER_NODE_LIB"
    TYPE_LIB_ENV = "SLITHER_TYPE_LIB"
    # env
    pluginBase = os.path.join(os.path.realpath(os.path.dirname(__file__)), "plugins")
    os.environ[NODE_LIB_ENV] = os.path.join(pluginBase, "nodes")
    os.environ[TYPE_LIB_ENV] = os.path.join(pluginBase, "datatypes")
    typeregistry.DataTypeRegistry()
    nodeRegistry.NodeRegistry()
    root = TestCompound("root")
    executor.StandardExecutor().execute(root)
    pprint.pprint(root.serialize())
    print root.execution.value()
