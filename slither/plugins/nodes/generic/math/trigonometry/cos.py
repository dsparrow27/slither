import math

from slither import api


class Cos(api.ComputeNode):
    Type = "Cos"
    category = "math"
    documentation = "cos"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self):
        self.output.setValue(math.cos(self.input.value()))
