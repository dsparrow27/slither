from slither.core import attribute
from slither.core import node


class StringNode(node.BaseNode):
    Type = "StringNode"
    category = "constant"
    documentation = "String constant"
    value = attribute.AttributeDefinition(isInput=True, type="str", default="")
    output = attribute.AttributeDefinition(isOutput=True, type="str", default="")

    def execute(self):
        self.output.setValue(str(self.input.value()))
