"""A simple test for nested compound networks
"""
import unittest

from slither import api


def createInputAttrDef(name, type_):
    return api.AttributeDefinition(name=name, input=True,
                                   type_=type_)


def createOutputAttrDef(name, type_):
    return api.AttributeDefinition(name=name,
                                   output=True,
                                   type_=type_)


class TestGraphStandardExecutor(unittest.TestCase):
    def setUp(self):
        self.graph = api.Graph()
        self.graph.initialize()
        self.executeType = self.graph.STANDARDEXECUTOR

    def test_compoundConnections(self):
        comp = self.graph.root.createNode("testCompound", "compound")
        comp.createAttribute(createInputAttrDef(name="testInput",
                                                type_=api.types.kFloat))
        comp.createAttribute(createOutputAttrDef(name="testOutput",
                                                 type_=api.types.kFloat))
        subChild = comp.createNode("subsubChild", "Sum")

        subChild.inputA.connect(comp.testInput)
        subChild.output.connect(comp.testOutput)
        self.graph.root.createAttribute(createOutputAttrDef("execution", api.types.kFloat))
        comp.testOutput.connect(self.graph.root.execution)
        comp.testInput.setValue(10)
        subChild.inputB.setValue(30)

        self.assertTrue(self.graph.root.hasChild("testCompound"))
        self.assertTrue(comp.hasChild("subsubChild"))
        self.assertTrue(comp.hasAttribute("testInput"))
        self.assertTrue(comp.hasAttribute("testOutput"))
        self.assertEquals(subChild.inputA.upstream, comp.testInput)
        self.assertEquals(comp.testOutput.upstream, subChild.output)
        self.graph.execute(self.graph.root, self.executeType)
        self.assertEquals(subChild.output.value(), 30.0)
        self.assertEquals(comp.testOutput.value(), 30.0)
        self.assertEquals(self.graph.root.execution.value(), 30)

    def test_deserialize(self):
        comp = self.graph.root.createNode("testCompound", "compound")
        comp.createAttribute(createInputAttrDef(name="testInput",
                                                type_=api.types.kFloat))
        comp.createAttribute(createOutputAttrDef(name="testOutput",
                                                 type_=api.types.kFloat))
        subChild = comp.createNode("subsubChild", "Sum")
        subChild.inputA.connect(comp.testInput)
        subChild.output.connect(comp.testOutput)
        self.graph.root.createAttribute(createOutputAttrDef("execution", api.types.kFloat))
        comp.testOutput.connect(self.graph.root.execution)
        comp.testInput.setValue(10)
        subChild.inputB.setValue(30)
        self.graph.execute(self.graph.root, self.executeType)
        serializeData = self.graph.serialize()
        newGraph = api.Graph()
        newGraph.initialize()
        newGraph.load(serializeData)
        self.assertEquals(len(newGraph.root.children), len(self.graph.root.children))
        self.assertTrue(newGraph.root.child("testCompound"))
        subChildNew = newGraph.root.child("testCompound")
        self.assertTrue(subChildNew.child("subsubChild"))
        self.assertTrue(subChildNew.hasAttribute("testInput"))
        self.assertTrue(subChildNew.hasAttribute("testOutput"))
        self.assertTrue(newGraph.root.hasAttribute("execution"))
        self.assertIsNotNone(subChildNew.child("subsubChild").inputA.upstream)
        self.assertEquals(subChildNew.child("subsubChild").inputA.upstream, comp.testInput)
        newGraph.execute(newGraph.root, self.executeType)
        self.assertEquals(subChildNew.child("subsubChild").output.value(), 30)
        self.assertEquals(subChildNew.testOutput.value(), 30)
        self.assertEquals(newGraph.root.execution.value(), 30)


if __name__ == "__main__":
    unittest.main()
