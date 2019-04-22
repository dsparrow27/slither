from slither import api


class Floor(api.ComputeNode):
    Type = "Floor"
    category = "math"
    documentation = "The floor of the input value"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(abs(self.input.value()))
