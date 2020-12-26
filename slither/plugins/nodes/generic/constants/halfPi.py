import math

from slither import api


class HalfPiNode(api.PXComputeNode):
    Type = "halfPi"
    def compute(self, context):
        context.output.setValue(math.pi * 0.5)
