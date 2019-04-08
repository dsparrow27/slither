from slither.core import attribute
from slither.core import node


class Invert(node.BaseNode):
    Type = "Invert"
    category = "math"
    documentation = "Multiplies the input values together"
    input = attribute.AttributeDefinition(isInput=True, type_="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_="float", default=0)

    def execute(self):
        self.output.setValue(self.input.value() * -1)
