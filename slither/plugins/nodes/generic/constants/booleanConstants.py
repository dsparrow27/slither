from slither import api


class Boolean(api.ComputeNode):
    Type = "bool"
    # category = "constant"
    # documentation = "boolean"
    # value = api.AttributeDefinition(type_=api.types.kBool, default=True, input=True)
    # output = api.AttributeDefinition(type_=api.types.kBool, default=True, output=True)

    def execute(self, context):
        context.output.setValue(bool(context.input.value()))
