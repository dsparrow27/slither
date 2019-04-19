import re

from slither import api


class Regex(api.ComputeNode):
    Type = "Regex"
    category = "string"
    documentation = "Returns a list of items the have the characters"
    strings = api.AttributeDefinition(isInput=True, type_=api.types.kString, array=True, default=[])
    searchString = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="")
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kString, array=True, default=[])

    def execute(self):
        self.output.setValue([char for char in self.strings.value() if re.search(self.searchString.value(), char)])
