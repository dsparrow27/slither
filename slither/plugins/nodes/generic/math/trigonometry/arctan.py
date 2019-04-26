import math

from slither import api


class ArcTan(api.ComputeNode):
    Type = "ArcTan"
    category = "math"
    documentation = "Arc tan"
    input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(math.atan(self.input.value()))
