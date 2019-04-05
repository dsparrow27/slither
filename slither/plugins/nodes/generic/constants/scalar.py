from slither.core import attribute
from slither.core import node


class Scalar(node.BaseNode):
    Type = "Scalar"
    category = "constant"
    documentation = "Scalar"
    value = attribute.AttributeDefinition(isInput=True, type="float", default=0.0)
    output = attribute.AttributeDefinition(isOutput=True, type="float", default=0.0)

    def execute(self):
        self.output.setValue(float(self.input.value()))
