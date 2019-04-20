import math

from slither import api


class SquareRoot(api.ComputeNode):
    Type = "SquareRoot"
    category = "math"
    documentation = "SquareRoot of the input values"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self):
        self.output.setValue(math.sqrt(self.input.value()))
