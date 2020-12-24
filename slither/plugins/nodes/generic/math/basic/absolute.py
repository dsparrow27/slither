from slither import api


class Floor(api.PXComputeNode):
    Type = "floor"
    # category = "math"
    # documentation = "The floor of the input value"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(abs(context.input.value()))
