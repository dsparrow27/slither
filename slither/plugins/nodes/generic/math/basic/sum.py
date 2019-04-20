from slither import api


class Sum(api.ComputeNode):
    Type = "Sum"
    category = "math"
    documentation = "Adds the input values together"
    inputA = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0.0)
    inputB = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0.0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0.0)

    def execute(self):
        self.output.setValue(self.inputA.value() + self.inputB.value())
