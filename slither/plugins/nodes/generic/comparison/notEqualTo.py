from slither import api


class NotEqualToNode(api.PXComputeNode):
    Type = "notEqualTo"
    # value1 = api.AttributeDefinition(api.types.kFloat, input=True)
    # value2 = api.AttributeDefinition(api.types.kFloat, input=True)
    # result = api.AttributeDefinition(api.types.kBool, output=True)

    def compute(self, context):
        result = context.value1.value() != context.value2.value()

        context.result.setValue(result)
