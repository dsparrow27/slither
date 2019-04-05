from slither.core import attribute
from slither.core import node


class Sum(node.BaseNode):
    Type = "Sum"
    category = "math"
    documentation = "Adds the input values together"
    inputA = attribute.AttributeDefinition(isInput=True, type="float", default=0)
    inputB = attribute.AttributeDefinition(isInput=True, type="float", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type="float", default=0)

    def execute(self):
        self.output.setValue(self.inputA.value() + self.inputB.value())