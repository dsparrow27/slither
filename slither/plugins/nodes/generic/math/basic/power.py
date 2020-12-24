from slither import api


class Power(api.PXComputeNode):
    Type = "power"
    # category = "math"
    # documentation = "power of the input values"
    # inputA = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # inputB = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(context.inputA.value() ** context.inputB.value())
