import math

from slither import api


class Sin(api.ComputeNode):
    Type = "Sin"
    category = "math"
    documentation = "sin"
    input = api.AttributeDefinition(isInput=True, type_="kFloat", default=0)
    output = api.AttributeDefinition(isOutput=True, type_="kFloat", default=0)

    def execute(self):
        self.output.setValue(math.sin(self.input.value()))
