import math

from slither.core import attribute
from slither.core import node


class ArcSin(node.BaseNode):
    category = "math"
    documentation = "Arc sin"
    input = attribute.AttributeDefinition(isInput=True,type_=float, default=0)
    output = attribute.AttributeDefinition(isOutput=True,type_=float, default=0)

    def execute(self):
        self.output.setValue(math.asin(self.input.value()))
