from slither.core import attribute
from slither.core import node


class Scalar(node.BaseNode):
    category = "constant"
    documentation = "Scalar"
    value = attribute.InputDefinition(type_=float, default=0.0)
    output = attribute.OutputDefinition(type_=float, default=0.0)

    def execute(self):
        self.output.setValue(float(self.input.value()))
