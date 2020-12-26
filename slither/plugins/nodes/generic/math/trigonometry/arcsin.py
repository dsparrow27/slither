import math

from slither import api


class ArcSin(api.PXComputeNode):
    Type = "arcSin"
    def compute(self, context):
        context.output.setValue(math.asin(context.input.value()))
