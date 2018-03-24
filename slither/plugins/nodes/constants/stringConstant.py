from slither.core import attribute
from slither.core import node


class StringNode(node.BaseNode):
    category = "constant"
    documentation = "String constant"
    value = attribute.InputDefinition(type_=str, default="")
    output = attribute.OutputDefinition(type_=str, default="")

    def execute(self):
        self.output.setValue(str(self.input.value()))
