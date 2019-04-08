import math

from slither.core import attribute
from slither.core import node


class Cos(node.BaseNode):
    Type = "Cos"
    category = "math"
    documentation = "cos"
    input = attribute.AttributeDefinition(isInput=True, type_="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_="float", default=0)

    def execute(self):
        self.output.setValue(math.cos(self.input.value()))
