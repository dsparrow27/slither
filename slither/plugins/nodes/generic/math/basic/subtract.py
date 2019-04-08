from slither.core import attribute
from slither.core import node


class Substract(node.BaseNode):
    Type = "Substract"
    category = "math"
    documentation = "subtracts the input values"
    inputA = attribute.AttributeDefinition(isInput=True, type_="float", default=0)
    inputB = attribute.AttributeDefinition(isInput=True, type_="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_="float", default=0)

    def execute(self):
        self.output.setValue(self.inputA.value() - self.inputB.value())
