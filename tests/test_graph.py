"""A simple test for nested compound networks
"""
import os
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
        self.app = api.Application()
        self.graph = self.app.createGraph("mainGraph")
        self.executeType = self.app.STANDARDEXECUTOR

    def testGraphLocalExecutor(self):
        testGraph = self.app.createGraph("localExecutor")
        testGraph.loadFromFile(os.path.join(os.path.dirname(__file__), "data", "testGraph.slgraph"))
        testGraph.execute(testGraph.root, self.app.STANDARDEXECUTOR)
        self.app.deleteGraph("localExecutor")

    def testGraphBackgroundExecutor(self):
        testGraph = self.app.createGraph("backgroundExecutor")
        testGraph.loadFromFile(os.path.join(os.path.dirname(__file__), "data", "testGraph.slgraph"))
        testGraph.execute(testGraph.root, self.app.PARALLELEXECUTOR)
        self.app.deleteGraph("backgroundExecutor")

    def test_compoundConnections(self):
        comp = self.graph.root.createNode("testCompound", "compound")
        comp.createAttribute(createInputAttrDef(name="testInput",
                                                type_=self.app.registry.dataTypeClass("kFloat")))
        comp.createAttribute(createOutputAttrDef(name="testOutput",
                                                 type_=self.app.registry.dataTypeClass("kFloat")))
        subChild = comp.createNode("subsubChild", "sum")

        subChild.inputA.connect(comp.testInput)
        subChild.output.connect(comp.testOutput)
        self.graph.root.createAttribute(createOutputAttrDef("execution", self.app.registry.dataTypeClass("kFloat")))
        comp.testOutput.connect(self.graph.root.execution)
        comp.testInput.setValue(10)
        subChild.inputB.setValue(30)

        self.assertTrue(self.graph.root.hasChild("testCompound"))
        self.assertTrue(comp.hasChild("subsubChild"))
        self.assertTrue(comp.hasAttribute("testInput"))
        self.assertTrue(comp.hasAttribute("testOutput"))
        self.assertEqual(subChild.inputA.upstream, comp.testInput)
        self.assertEqual(comp.testOutput.upstream, subChild.output)
        self.graph.execute(self.graph.root, self.executeType)
        self.assertEqual(subChild.output.value(), 30.0)
        self.assertEqual(comp.testOutput.value(), 30.0)
        self.assertEqual(self.graph.root.execution.value(), 30)

    def test_deserialize(self):
        comp = self.graph.root.createNode("testCompound", "compound")
        comp.createAttribute(createInputAttrDef(name="testInput",
                                                type_=self.app.registry.dataTypeClass("kFloat")))
        comp.createAttribute(createOutputAttrDef(name="testOutput",
                                                 type_=self.app.registry.dataTypeClass("kFloat")))
        subChild = comp.createNode("subsubChild", "sum")
        subChild.inputA.connect(comp.testInput)
        subChild.output.connect(comp.testOutput)
        self.graph.root.createAttribute(createOutputAttrDef("execution", self.app.registry.dataTypeClass("kFloat")))
        comp.testOutput.connect(self.graph.root.execution)
        comp.testInput.setValue(10)
        subChild.inputB.setValue(30)
        self.graph.execute(self.graph.root, self.executeType)
        self.assertEqual(self.graph.root.execution.value(), 30)
        serializeData = self.graph.serialize()
        newGraph = self.app.createGraph("newGraph")
        newGraph.load(serializeData)
        self.assertEqual(len(newGraph.root.children), len(self.graph.root.children))
        self.assertTrue(newGraph.root.child("testCompound"))
        subChildNew = newGraph.root.child("testCompound")
        self.assertTrue(subChildNew.child("subsubChild"))
        self.assertTrue(subChildNew.hasAttribute("testInput"))
        self.assertTrue(subChildNew.hasAttribute("testOutput"))
        self.assertTrue(newGraph.root.hasAttribute("execution"))
        self.assertIsNotNone(subChildNew.child("subsubChild").inputA.upstream)
        newGraph.execute(newGraph.root, self.executeType)
        self.assertEqual(subChildNew.child("subsubChild").output.value(), 30)
        self.assertEqual(subChildNew.testOutput.value(), 30)
        self.assertIsNotNone(newGraph.root.execution.upstream)
        self.assertEqual(newGraph.root.execution.value(), 30)
        self.app.deleteGraph("newGraph")

        testGraph = self.app.createGraph("testGraph")
        testGraph.loadFromFile(os.path.join(os.path.dirname(__file__), "data", "testGraph.slgraph"))
        self.app.deleteGraph("testGraph")


if __name__ == "__main__":
    unittest.main()
