"""A simple test for nested compound networks
"""
import pprint
import unittest

from slither import api


def createInputAttrDef(name, type_):
    return api.AttributeDefinition(name=name, isInput=True,
                                   type_=type_)


def createOutputAttrDef(name, type_):
    return api.AttributeDefinition(name=name,
                                   isOutput=True,
                                   type_=type_)


class TestGraphStandardExecutor(unittest.TestCase):
    def setUp(self):
        self.app = api.application.Application()
        self.app.initialize()
        self.executeType = self.app.STANDARDEXECUTOR

    def test_compoundConnections(self):
        comp = self.app.root.createNode("testCompound", "compound")
        comp.createAttribute(createInputAttrDef(name="testInput",
                                                type_=api.types.kFloat))
        comp.createAttribute(createOutputAttrDef(name="testOutput",
                                                 type_=api.types.kFloat))
        subChild = comp.createNode("subsubChild", "Sum")

        subChild.inputA.connectUpstream(comp.testInput)
        comp.testOutput.connectUpstream(subChild.output)
        self.app.root.createAttribute(createOutputAttrDef("execution", api.types.kFloat))
        self.app.root.execution.connectUpstream(comp.testOutput)
        comp.testInput.setValue(10)
        subChild.inputB.setValue(30)
        self.app.execute(self.app.root, self.executeType)
        self.assertEquals(subChild.inputA.upstream, comp.testInput)
        self.assertEquals(subChild.output.value(), 30)
        self.assertEquals(comp.testOutput.value(), 30)
        self.assertEquals(self.app.root.execution.value(), 30)

        pprint.pprint(self.app.root.serialize())

if __name__ == "__main__":
    unittest.main()
