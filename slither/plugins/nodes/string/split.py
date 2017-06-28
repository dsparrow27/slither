from slither.core import attribute
from slither.core import node


class SplitString(node.BaseNode):
    category = "string"
    documentation = "splits a string by a delimiter"
    string = attribute.InputDefinition(type_=str, default="")
    delimiter = attribute.InputDefinition(type_=str, default=",")
    output = attribute.OutputDefinition(type_=str, array=True, default="")

    def execute(self):
        self.output.setValue(self.input.value().split(self.delimiter.value()))
