import math

from slither.core import attribute
from slither.core import node


class Floor(node.BaseNode):
    Type = "Floor"
    category = "math"
    documentation = "The floor of the input value"
    input = attribute.AttributeDefinition(isInput=True, type_="float", default=0, doc="The value to floor")
    output = attribute.AttributeDefinition(isOutput=True, type_="float", default=0, doc="The result of the floor")

    def execute(self):
        self.output.setValue(math.floor(self.input.value()))
