import re

from slither.core import attribute
from slither.core import node


class SubStringNode(node.BaseNode):
    """Returns a list of strings that have the search string in it.
    """
    Type = "SubStringNode"
    category = "string"
    documentation = __doc__
    value = attribute.AttributeDefinition(isInput=True, type="str", default="", array=True)
    search = attribute.AttributeDefinition(isInput=True, type="str", default="")
    replace = attribute.AttributeDefinition(isInput=True, type="str", default="")
    output = attribute.AttributeDefinition(isOutput=True, type="str", array=True, default=[])

    def execute(self):
        result = [re.sub(self.self.search.value(), self.replace.value(), char) for char in
                  self.valuePlug_.value()]
        self.output.setValue(result)
        return result
