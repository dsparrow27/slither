from slither.core import attribute
from slither.core import node


class Dictionary(node.BaseNode):
    category = "constant"
    documentation = "Dictionary"
    input = attribute.OutputDefinition(type_=dict, default=dict())
    output = attribute.OutputDefinition(type_=dict, default=dict())

    def execute(self):
        self.output.setValue(dict(self.input.value()))

