import math

from slither import api


class Sin(api.ComputeNode):
    Type = "Sin"
    category = "math"
    documentation = "sin"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(math.sin(self.input.value()))
