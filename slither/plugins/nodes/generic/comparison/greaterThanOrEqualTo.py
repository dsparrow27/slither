from slither import api


class GreaterThanOrEqualToNode(api.PXComputeNode):
    Type = "greaterThanOrEqualTo"
    # value1 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    # value2 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    # result = api.AttributeDefinition(type_=api.types.kBool, output=True)

    def compute(self, context):
        result = context.value1Plug_ >= context.value2Plug_
        context.result.setValue(result)
