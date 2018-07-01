from slither.core import attribute
from slither.core import node


class Floor(node.BaseNode):
    category = "math"
    documentation = "The floor of the input value"
    input = attribute.AttributeDefinition(isInput=True,type_=float, default=0)
    output = attribute.AttributeDefinition(isOutput=True,type_=float, default=0)

    def execute(self):
        self.output.setValue(abs(self.input.value()))
