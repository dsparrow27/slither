import re

from slither.core import attribute
from slither.core import node


class Regex(node.BaseNode):
    Type = "Regex"
    category = "string"
    documentation = "Returns a list of items the have the characters"
    strings = attribute.AttributeDefinition(isInput=True, type_="str", array=True, default=[])
    searchString = attribute.AttributeDefinition(isInput=True, type_="str", default="")
    output = attribute.AttributeDefinition(isOutput=True, type_="str", array=True, default=[])

    def execute(self):
        self.output.setValue([char for char in self.strings.value() if re.search(self.searchString.value(), char)])
