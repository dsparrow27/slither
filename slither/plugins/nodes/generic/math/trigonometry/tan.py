import math

from slither.core import attribute
from slither.core import node


class Tan(node.BaseNode):
    Type = "Tan"
    category = "math"
    documentation = "tan"
    input = attribute.AttributeDefinition(isInput=True, type="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type="float", default=0)

    def execute(self):
        self.output.setValue(math.tan(self.input.value()))
