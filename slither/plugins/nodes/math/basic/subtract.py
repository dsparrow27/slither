from slither.core import attribute
from slither.core import node


class Substract(node.BaseNode):
    category = "math"
    documentation = "subtracts the input values"
    inputA = attribute.InputDefinition(type_=float, default=0)
    inputB = attribute.InputDefinition(type_=float, default=0)
    output = attribute.OutputDefinition(type_=float, default=0)

    def execute(self):
        self.output.setValue(self.inputA.value() - self.inputB.value())
