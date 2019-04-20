from slither import api


class Divide(api.ComputeNode):
    Type = "Divide"
    category = "math"
    documentation = "Divides the input values together, raises ZooDivisionError if dividing by 0"
    inputA = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    inputB = api.AttributeDefinition(isInput=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFloat, default=0)

    def execute(self):
        # @todo log
        try:
            self.output.setValue(self.inputA.value() / self.inputB.value())
        except ZeroDivisionError:
            raise
