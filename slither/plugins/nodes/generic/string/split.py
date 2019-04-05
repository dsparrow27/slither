from slither.core import attribute
from slither.core import node


class SplitString(node.BaseNode):
    Type = "SplitString"
    category = "string"
    documentation = "splits a string by a delimiter"
    string = attribute.AttributeDefinition(isInput=True, type="str", default="")
    delimiter = attribute.AttributeDefinition(isInput=True, type="str", default=",")
    output = attribute.AttributeDefinition(isOutput=True, type="str", array=True, default="")

    def execute(self):
        self.output.setValue(self.input.value().split(self.delimiter.value()))
