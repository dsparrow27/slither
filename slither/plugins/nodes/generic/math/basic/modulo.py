from slither import api


class Modulo(api.ComputeNode):
    Type = "modulo"
    # category = "math"
    # documentation = "Multiplies the input values together"
    # inputA = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # inputB = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0)

    def execute(self, context):
        context.output.setValue(context.inputA.value() % context.inputB.value())
