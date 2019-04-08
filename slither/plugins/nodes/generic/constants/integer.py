from slither.core import attribute
from slither.core import node


class Integer(node.BaseNode):
    Type = "Integer"
    category = "constant"
    documentation = "integer"
    value = attribute.AttributeDefinition(isInput=True, type_="int", default=0)
    output = attribute.AttributeDefinition(isOutput=True, type_="int", default=0)

    def execute(self):
        self.output.setValue(int(self.input.value()))
