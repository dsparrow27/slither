from slither import api


class Invert(api.ComputeNode):
    Type = "Invert"
    category = "math"
    documentation = "Multiplies the input values together"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self):
        self.output.setValue(self.input.value() * -1)
