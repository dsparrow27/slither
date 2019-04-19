from slither import api


class Power(api.ComputeNode):
    Type = "Power"
    category = "math"
    documentation = "power of the input values"
    inputA = api.AttributeDefinition(isInput=True, type_="kFloat", default=0)
    inputB = api.AttributeDefinition(isInput=True, type_="kFloat", default=0)
    output = api.AttributeDefinition(isOutput=True, type_="kFloat", default=0)

    def execute(self):
        self.output.setValue(self.inputA.value() ** self.inputB.value())
