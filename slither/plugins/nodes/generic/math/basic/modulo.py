from slither import api


class Modulo(api.ComputeNode):
    Type = "Modulo"
    category = "math"
    documentation = "Multiplies the input values together"
    inputA = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    inputB = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        self.output.setValue(self.inputA.value() % self.inputB.value())
