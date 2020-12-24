import math

from slither import api


class HalfPiNode(api.PXComputeNode):
    Type = "halfPi"
    # category = "constant"
    # documentation = "HalfPi"
    # output = api.AttributeDefinition(output=True, type_=api.types.kBool, default=True)

    def compute(self, context):
        context.output.setValue(math.pi * 0.5)
