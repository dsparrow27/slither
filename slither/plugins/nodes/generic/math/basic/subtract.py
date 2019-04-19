from slither import api


class Substract(api.ComputeNode):
    Type = "Substract"
    category = "math"
    documentation = "subtracts the input values"
    inputA = api.AttributeDefinition(isInput=True, type_="kFloat", default=0)
    inputB = api.AttributeDefinition(isInput=True, type_="kFloat", default=0)
    output = api.AttributeDefinition(isOutput=True, type_="kFloat", default=0)

    def execute(self):
        self.output.setValue(self.inputA.value() - self.inputB.value())
