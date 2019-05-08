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
                                   output=True,
                                   type_=type_)


class TestGraphStandardExecutor(unittest.TestCase):
    def setUp(self):
        self.app = api.graph.Graph()
        self.app.initialize()
        self.executeType = self.app.STANDARDEXECUTOR

    def test_compoundConnections(self):
        comp = self.app.root.createNode("testCompound", "compound")
        comp.createAttribute(createInputAttrDef(name="testInput",
                                                type_=api.types.kFloat))
        comp.createAttribute(createOutputAttrDef(name="testOutput",
                                                 type_=api.types.kFloat))
        subChild = comp.createNode("subsubChild", "Sum")

        subChild.inputA.connect(comp.testInput)
        comp.testOutput.connect(subChild.output)
        self.app.root.createAttribute(createOutputAttrDef("execution", api.types.kFloat))
        self.app.root.execution.connect(comp.testOutput)
        comp.testInput.setValue(10)
        subChild.inputB.setValue(30)

        self.assertTrue(self.app.root.hasChild("testCompound"))
        self.assertTrue(comp.hasChild("subsubChild"))
        self.assertTrue(comp.hasAttribute("testInput"))
        self.assertTrue(comp.hasAttribute("testOutput"))
        self.assertEquals(subChild.inputA.upstream, comp.testInput)
        self.assertEquals(comp.testOutput.upstream, subChild.output)
        self.app.execute(self.app.root, self.executeType)
        self.assertEquals(subChild.output.value(), 30.0)
        self.assertEquals(comp.testOutput.value(), 30.0)
        self.assertEquals(self.app.root.execution.value(), 30)

    def test_deserialize(self):
        comp = self.app.root.createNode("testCompound", "compound")
        comp.createAttribute(createInputAttrDef(name="testInput",
                                                type_=api.types.kFloat))
        comp.createAttribute(createOutputAttrDef(name="testOutput",
                                                 type_=api.types.kFloat))
        subChild = comp.createNode("subsubChild", "Sum")

        subChild.inputA.connect(comp.testInput)
        comp.testOutput.connect(subChild.output)
        self.app.root.createAttribute(createOutputAttrDef("execution", api.types.kFloat))
        self.app.root.execution.connect(comp.testOutput)
        comp.testInput.setValue(10)
        subChild.inputB.setValue(30)
        self.app.execute(self.app.root, self.executeType)
        serializeData = self.app.serialize()
        newApp = api.graph.Graph()
        newApp.initialize()
        newApp.load(serializeData)
        # pprint.pprint(newApp.serialize())
        self.assertEquals(len(newApp.root.children), len(self.app.root.children))
        self.assertTrue(newApp.root.child("testCompound"))
        subChildNew = newApp.root.child("testCompound")
        self.assertTrue(subChildNew.child("subsubChild"))
        self.assertTrue(subChildNew.hasAttribute("testInput"))
        self.assertTrue(subChildNew.hasAttribute("testOutput"))
        self.assertTrue(newApp.root.hasAttribute("execution"))
        self.assertEquals(subChildNew.child("subsubChild").inputA.upstream, comp.testInput)
        newApp.execute(newApp.root, self.executeType)
        self.assertEquals(subChildNew.child("subsubChild").output.value(), 30)
        self.assertEquals(subChildNew.testOutput.value(), 30)
        self.assertEquals(newApp.root.execution.value(), 30)


if __name__ == "__main__":
    unittest.main()
