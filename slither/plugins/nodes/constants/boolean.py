from slither.core import attribute
from slither.core import node


class Boolean(node.BaseNode):
    category = "constant"
    documentation = "boolean"
    value = attribute.InputDefinition(type_=bool, default=True)
    output = attribute.OutputDefinition(type_=bool, default=True)

    def execute(self):
        self.output.setValue(bool(self.input.value()))
