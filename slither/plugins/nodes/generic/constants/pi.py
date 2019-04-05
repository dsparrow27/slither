import math

from slither.core import attribute
from slither.core import node


class Pi(node.BaseNode):
    Type = "Pi"
    category = "constant"
    documentation = "Pi"
    output = attribute.AttributeDefinition(isOutput=True, type="bool", default=True)

    def execute(self):
        self.output.setValue(math.pi)
