from slither import api


class GreaterThanNode(api.PXComputeNode):
    Type = "greaterThan"
    def compute(self, context):
        result = context.value1.value() > context.value2.value()

        context.result.setValue(result)
