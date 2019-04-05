from slither.core import attribute
from slither.core import node


class Dictionary(node.BaseNode):
    Type = "Dictionary"
    category = "constant"
    documentation = "Dictionary"
    input = attribute.AttributeDefinition(isOutput=False, type="dict", default=dict())
    output = attribute.AttributeDefinition(isOutput=True, type="dict", default=dict())

    def execute(self):
        self.output.setValue(dict(self.input.value()))
