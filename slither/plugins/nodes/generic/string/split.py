from slither import api


class SplitString(api.PXComputeNode):
    Type = "splitString"

    def compute(self, context):
        context.output.setValue(context.input.value().split(context.delimiter.value()))
