from slither.core import attribute
from slither.core import node


class Boolean(node.BaseNode):
    Type = "Boolean"
    category = "constant"
    documentation = "boolean"
    value = attribute.AttributeDefinition(type_="bool", default=True, isInput=True)
    output = attribute.AttributeDefinition(type_="bool", default=True, isOutput=True)

    def execute(self):
        self.output.setValue(bool(self.input.value()))
