import math

from slither import api


class SquareRoot(api.PXComputeNode):
    Type = "squareRoot"
    def compute(self, context):
        context.output.setValue(math.sqrt(context.input.value()))
