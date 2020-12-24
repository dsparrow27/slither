import math

from slither import api


class ArcTan(api.PXComputeNode):
    Type = "arcTan"
    # category = "math"
    # documentation = "Arc tan"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(math.atan(context.input.value()))
