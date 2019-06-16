from slither import api


class LessThanOrEqualToNode(api.ComputeNode):
    Type = "LessThanOrEqualToNode"
    value1 = api.AttributeDefinition(api.types.kFloat, input=True)
    value2 = api.AttributeDefinition(api.types.kFloat, input=True)
    result = api.AttributeDefinition(api.types.kBool, output=True)

    def execute(self, context):
        result = context.value1.value() <= context.value2.value()

        context.result.setValue(result)
