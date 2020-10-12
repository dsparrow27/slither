import math

from slither import api


class ArcCos(api.ComputeNode):
    Type = "arcCos"
    # category = "math"
    # documentation = "Arc cos"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        context.output.setValue(math.acos(context.input.value()))
