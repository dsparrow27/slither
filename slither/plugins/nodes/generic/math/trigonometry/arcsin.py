import math

from slither import api


class ArcSin(api.PXComputeNode):
    Type = "arcSin"
    # category = "math"
    # documentation = "Arc sin"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(math.asin(context.input.value()))
