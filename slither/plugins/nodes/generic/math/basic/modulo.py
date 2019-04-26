from slither import api


class Modulo(api.ComputeNode):
    Type = "Modulo"
    category = "math"
    documentation = "Multiplies the input values together"
    inputA = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    inputB = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(self.inputA.value() % self.inputB.value())
