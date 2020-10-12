from slither import api


class Sum(api.ComputeNode):
    Type = "sum"
    # category = "math"
    # documentation = "Adds the input values together"
    # inputA = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0.0)
    # inputB = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0.0)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0.0)

    def execute(self, context):
        context.output.setValue(context.inputA.value() + context.inputB.value())
