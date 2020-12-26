from slither import api


class NotEqualToNode(api.PXComputeNode):
    Type = "notEqualTo"

    def compute(self, context):
        result = context.value1.value() != context.value2.value()

        context.result.setValue(result)
