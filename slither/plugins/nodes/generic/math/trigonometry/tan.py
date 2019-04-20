import math

from slither import api


class Tan(api.ComputeNode):
    Type = "Tan"
    category = "math"
    documentation = "tan"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self):
        self.output.setValue(math.tan(self.input.value()))
