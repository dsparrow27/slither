from slither import api


class EqualToNode(api.PXComputeNode):
    Type = "equalTo"

    def compute(self, context):
        result = context.value1.value() == context.value2.value()
        context.result.setValue(result)
