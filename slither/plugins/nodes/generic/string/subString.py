import re

from slither import api


class SubStringNode(api.ComputeNode):
    """Returns a list of strings that have the search string in it.
    """
    Type = "SubStringNode"
    category = "string"
    documentation = __doc__
    value = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="", array=True)
    search = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="")
    replace = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="")
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kString, array=True, default=[])

    def execute(self):
        result = [re.sub(self.self.search.value(), self.replace.value(), char) for char in
                  self.valuePlug_.value()]
        self.output.setValue(result)
        return result
