import math

from slither import api


class SquareRoot(api.PXComputeNode):
    Type = "squareRoot"
    # category = "math"
    # documentation = "SquareRoot of the input values"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(math.sqrt(context.input.value()))
