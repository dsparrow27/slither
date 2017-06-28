from slither.core import attribute
from slither.core import node


class Multiply(node.BaseNode):
    category = "math"
    documentation = "Multiplies the input values together"
    inputA = attribute.InputDefinition(type_=float, default=0)
    inputB = attribute.InputDefinition(type_=float, default=0)
    output = attribute.OutputDefinition(type_=float, default=0)

    def execute(self):
        self.output.setValue(self.inputA.value() * self.inputB.value())
