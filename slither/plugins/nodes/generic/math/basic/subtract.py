from slither import api


class Substract(api.ComputeNode):
    Type = "Substract"
    category = "math"
    documentation = "subtracts the input values"
    inputA = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    inputB = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        context.output.setValue(context.inputA.value() - context.inputB.value())
