from slither.core import attribute
from slither.core import node


class String(node.BaseNode):
    category = "math"
    documentation = "string value"
    string = attribute.InputDefinition(type_=str, default="")
    output = attribute.OutputDefinition(type_=str, default="")

    def execute(self):
        self.output.setValue(str(self.input.value()))
