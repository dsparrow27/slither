import math

from slither import api


class HalfPiNode(api.ComputeNode):
    Type = "HalfPiNode"
    category = "constant"
    documentation = "HalfPiNode"
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kBoolean, default=True)

    def execute(self):
        self.output.setValue(math.pi * 0.5)
