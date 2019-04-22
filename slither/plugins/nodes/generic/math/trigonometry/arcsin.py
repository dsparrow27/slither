import math

from slither import api


class ArcSin(api.ComputeNode):
    Type = "ArcSin"
    category = "math"
    documentation = "Arc sin"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(math.asin(self.input.value()))
