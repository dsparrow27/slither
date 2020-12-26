import math

from slither import api


class ArcTan(api.PXComputeNode):
    Type = "arcTan"
    def compute(self, context):
        context.output.setValue(math.atan(context.input.value()))
