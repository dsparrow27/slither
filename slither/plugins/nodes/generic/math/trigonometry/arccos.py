import math

from slither import api


class ArcCos(api.PXComputeNode):
    Type = "arcCos"
    def compute(self, context):
        context.output.setValue(math.acos(context.input.value()))
