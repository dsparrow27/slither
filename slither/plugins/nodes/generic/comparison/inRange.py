from slither import api


class InRangeNode(api.PXComputeNode):
    Type = "inRange"
    def compute(self, context):
        result = context.value1.value() in range(context.value2.value())

        context.result.setValue(result)
