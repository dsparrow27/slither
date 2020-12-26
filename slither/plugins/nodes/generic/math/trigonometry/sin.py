import math

from slither import api


class Sin(api.PXComputeNode):
    Type = "sin"

    def compute(self, context):
        context.output.setValue(math.sin(context.input.value()))
