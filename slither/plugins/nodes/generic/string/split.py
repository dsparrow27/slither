from slither import api


class SplitString(api.ComputeNode):
    Type = "splitString"

    def execute(self, context):
        context.output.setValue(context.input.value().split(context.delimiter.value()))
