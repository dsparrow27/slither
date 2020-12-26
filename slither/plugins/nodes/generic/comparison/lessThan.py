from slither import api


class LessThanNode(api.PXComputeNode):
    Type = "lessThan"
    def compute(self, context):
        result = context.value1.value() < context.value2.value()
        context.result.setValue(result)
