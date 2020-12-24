from slither import api


class Invert(api.PXComputeNode):
    Type = "invert"
    # category = "math"
    # documentation = "Multiplies the input values together"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(context.input.value() * -1)
