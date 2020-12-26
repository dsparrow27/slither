import math

from slither import api


class Tan(api.PXComputeNode):
    Type = "tan"

    def compute(self, context):
        context.output.setValue(math.tan(context.input.value()))
