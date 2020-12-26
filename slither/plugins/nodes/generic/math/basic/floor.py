import math

from slither import api


class Floor(api.PXComputeNode):
    Type = "floor"
    def compute(self, context):
        context.output.setValue(math.floor(context.input.value()))
