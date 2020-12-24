from slither import api


class StringNode(api.PXComputeNode):
    Type = "string"

    def compute(self, context):
        context.output.setValue(str(context.value.value()))
