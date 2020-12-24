import math

from slither import api


class Sin(api.PXComputeNode):
    Type = "sin"
    # category = "math"
    # documentation = "sin"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def compute(self, context):
        context.output.setValue(math.sin(context.input.value()))
