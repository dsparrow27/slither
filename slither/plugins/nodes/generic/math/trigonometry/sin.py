import math

from slither.core import attribute
from slither.core import node


class Sin(node.BaseNode):
    Type = "Sin"
    category = "math"
    documentation = "sin"
    input = attribute.AttributeDefinition(isInput=True, type="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type="float", default=0)

    def execute(self):
        self.output.setValue(math.sin(self.input.value()))