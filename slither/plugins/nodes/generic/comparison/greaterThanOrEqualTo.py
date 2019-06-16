from slither import api


class GreaterThanOrEqualToNode(api.ComputeNode):
    Type = "greaterThanOrEqualToNode"
    value1 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    value2 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    result = api.AttributeDefinition(type_=api.types.kBool, output=True)

    def execute(self, context):
        result = context.value1Plug_ >= context.value2Plug_
        context.result.setValue(result)
