import math

from slither import api


class Pi(api.PXComputeNode):
    Type = "pi"
    # category = "constant"
    # documentation = "Pi"
    # output = api.AttributeDefinition(output=True, type_=api.types.kBool, default=True)

    def compute(self, context):
        context.output.setValue(math.pi)
