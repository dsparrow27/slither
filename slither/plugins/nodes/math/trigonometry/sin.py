import math

from slither.core import attribute
from slither.core import node


class Sin(node.BaseNode):
    category = "math"
    documentation = "sin"
    input = attribute.AttributeDefinition(isInput=True,type_=float, default=0)
    output = attribute.AttributeDefinition(isOutput=True,type_=float, default=0)

    def execute(self):
        self.output.setValue(math.sin(self.input.value()))
