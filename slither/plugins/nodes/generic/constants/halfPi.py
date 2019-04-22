import math

from slither import api


class HalfPiNode(api.ComputeNode):
    Type = "HalfPiNode"
    category = "constant"
    documentation = "HalfPiNode"
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kBool, default=True)

    def execute(self, context):
        self.output.setValue(math.pi * 0.5)
