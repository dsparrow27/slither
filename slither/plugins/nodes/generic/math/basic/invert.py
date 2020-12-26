from slither import api


class Invert(api.PXComputeNode):
    Type = "invert"
    def compute(self, context):
        context.output.setValue(context.input.value() * -1)
