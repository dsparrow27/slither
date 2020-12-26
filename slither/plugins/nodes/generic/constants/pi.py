import math

from slither import api


class Pi(api.PXComputeNode):
    Type = "pi"
    def compute(self, context):
        context.output.setValue(math.pi)
