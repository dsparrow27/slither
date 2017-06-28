import math

from slither.core import attribute
from slither.core import node


class Tan(node.BaseNode):
    category = "math"
    documentation = "tan"
    input = attribute.InputDefinition(type_=float, default=0)
    output = attribute.OutputDefinition(type_=float, default=0)

    def execute(self):
        self.output.setValue(math.tan(self.input.value()))