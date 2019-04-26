import math

from slither import api


class SquareRoot(api.ComputeNode):
    Type = "SquareRoot"
    category = "math"
    documentation = "SquareRoot of the input values"
    input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(math.sqrt(self.input.value()))
