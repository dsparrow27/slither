from slither import api


class LessThanOrEqualToNode(api.PXComputeNode):
    Type = "lessThanOrEqualTo"

    def compute(self, context):
        result = context.value1.value() <= context.value2.value()

        context.result.setValue(result)
