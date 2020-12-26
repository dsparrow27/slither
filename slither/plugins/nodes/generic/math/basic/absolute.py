from slither import api


class Floor(api.PXComputeNode):
    Type = "floor"
    def compute(self, context):
        context.output.setValue(abs(context.input.value()))
