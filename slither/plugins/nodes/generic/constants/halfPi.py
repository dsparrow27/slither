import math

from slither.core import attribute
from slither.core import node


class HalfPiNode(node.BaseNode):
    Type = "HalfPiNode"
    category = "constant"
    documentation = "HalfPiNode"
    output = attribute.AttributeDefinition(isOutput=True, type_="bool", default=True)

    def execute(self):
        self.output.setValue(math.pi * 0.5)
