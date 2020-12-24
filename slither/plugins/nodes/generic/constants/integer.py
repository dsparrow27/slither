from slither import api


class Integer(api.PXComputeNode):
    Type = "integer"
    # category = "constant"
    # documentation = "integer"
    # value = api.AttributeDefinition(input=True, type_=api.types.kInt, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kInt, default=0)

    def compute(self, context):
        context.output.setValue(int(context.input.value()))
