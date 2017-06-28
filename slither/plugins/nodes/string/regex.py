import re

from slither.core import attribute
from slither.core import node

class Regex(node.BaseNode):
    category = "string"
    documentation = "Returns a list of items the have the characters"
    strings = attribute.InputDefinition(type_=str, array=True, default=[])
    searchString = attribute.InputDefinition(type_=str, default="")
    output = attribute.OutputDefinition(type_=str, array=True, default=[])

    def execute(self):
        self.output.setValue([char for char in self.strings.value() if re.search(self.searchString.value(), char)])
