from slither.core import attribute
from slither.core import node


class Floor(node.BaseNode):
    Type = "Floor"
    category = "math"
    documentation = "The floor of the input value"
    input = attribute.AttributeDefinition(isInput=True, type="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type="float", default=0)

    def execute(self):
        self.output.setValue(abs(self.input.value()))
