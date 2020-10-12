import math

from slither import api


class HalfPiNode(api.ComputeNode):
    Type = "halfPi"
    # category = "constant"
    # documentation = "HalfPi"
    # output = api.AttributeDefinition(output=True, type_=api.types.kBool, default=True)

    def execute(self, context):
        context.output.setValue(math.pi * 0.5)
