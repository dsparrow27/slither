import math

from slither import api


class Floor(api.ComputeNode):
    Type = "Floor"
    category = "math"
    documentation = "The floor of the input value"
    input = api.AttributeDefinition(isInput=True, type_="kFloat", default=0, doc="The value to floor")
    output = api.AttributeDefinition(isOutput=True, type_="kFloat", default=0, doc="The result of the floor")

    def execute(self):
        self.output.setValue(math.floor(self.input.value()))
