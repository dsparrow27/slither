from slither import api


class GreaterThanNode(api.ComputeNode):
    Type = "greaterThan"
    # value1 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    # value2 = api.AttributeDefinition(type_=api.types.kFloat, input=True)
    # result = api.AttributeDefinition(type_=api.types.kBool, output=True)

    def execute(self, context):
        result = context.value1.value() > context.value2.value()

        context.result.setValue(result)
