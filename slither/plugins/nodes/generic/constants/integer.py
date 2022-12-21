from slither import api


class Integer(api.PXComputeNode):
    Type = "integer"
    def compute(self, context):
        context.output.setValue(int(context.value.value()))
