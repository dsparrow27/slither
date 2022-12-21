import re

from slither import api


class SubStringNode(api.PXComputeNode):
    """Returns a list of strings that have the search string in it.
    """
    Type = "subString"
    def compute(self, context):
        result = [re.sub(context.search.value(), context.replace.value(), char) for char in
                  context.value.value()]
        context.output.setValue(result)
        return result
