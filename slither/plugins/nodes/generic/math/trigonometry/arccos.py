import math

from slither import api


class ArcCos(api.ComputeNode):
    Type = "ArcCos"
    category = "math"
    documentation = "Arc cos"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(math.acos(self.input.value()))
