from slither import api


class Boolean(api.PXComputeNode):
    Type = "bool"

    def compute(self, context):
        context.output.setValue(bool(context.input.value()))
