import re

from slither import api


class Regex(api.ComputeNode):
    Type = "regex"

    def execute(self, context):
        context.output.setValue([char for char in context.strings.value() if re.search(context.searchString.value(), char)])
