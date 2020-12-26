import math
import os

from slither import api


class Rename(api.PXComputeNode):
    Type = "rename"
    def compute(self, context):
        context.output.setValue(math.pi)
        os.rename(context.file.value(), context.name.value())
