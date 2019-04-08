import math

from slither.core import attribute
from slither.core import node


class ArcCos(node.BaseNode):
    Type = "ArcCos"
    category = "math"
    documentation = "Arc cos"
    input = attribute.AttributeDefinition(isInput=True, type_="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_="float", default=0)

    def execute(self):
        self.output.setValue(math.acos(self.input.value()))
