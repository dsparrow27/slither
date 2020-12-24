import math

from slither import api


class Tan(api.PXComputeNode):
    Type = "tan"
    # category = "math"
    # documentation = "tan"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(math.tan(context.input.value()))
