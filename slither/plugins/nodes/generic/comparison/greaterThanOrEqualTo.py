from slither import api


class GreaterThanOrEqualToNode(api.PXComputeNode):
    Type = "greaterThanOrEqualTo"

    def compute(self, context):
        result = context.value1Plug_ >= context.value2Plug_
        context.result.setValue(result)
