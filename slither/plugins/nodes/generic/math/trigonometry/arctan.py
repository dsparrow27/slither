import math

from slither.core import attribute
from slither.core import node


class ArcTan(node.BaseNode):
    Type = "ArcTan"
    category = "math"
    documentation = "Arc tan"
    input = attribute.AttributeDefinition(isInput=True, type="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type="float", default=0)

    def execute(self):
        self.output.setValue(math.atan(self.input.value()))
