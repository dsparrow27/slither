import math

from slither.core import attribute
from slither.core import node


class SquareRoot(node.BaseNode):
    category = "math"
    documentation = "SquareRoot of the input values"
    input = attribute.AttributeDefinition(isInput=True,type_=float, default=0)
    output = attribute.AttributeDefinition(isOutput=True,type_=float, default=0)

    def execute(self):
        self.output.setValue(math.sqrt(self.input.value()))
