import math

from slither import api


class Cos(api.PXComputeNode):
    Type = "cos"
    def compute(self, context):
        context.output.setValue(math.cos(context.input.value()))
