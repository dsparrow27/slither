import math

from slither import api


class Cos(api.ComputeNode):
    Type = "cos"
    # category = "math"
    # documentation = "cos"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        context.output.setValue(math.cos(context.input.value()))
