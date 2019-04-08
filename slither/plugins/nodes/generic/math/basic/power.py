from slither.core import attribute
from slither.core import node


class Power(node.BaseNode):
    Type = "Power"
    category = "math"
    documentation = "power of the input values"
    inputA = attribute.AttributeDefinition(isInput=True, type_="float", default=0)
    inputB = attribute.AttributeDefinition(isInput=True, type_="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_="float", default=0)

    def execute(self):
        self.output.setValue(self.inputA.value() ** self.inputB.value())
