import math

from slither import api


class Floor(api.ComputeNode):
    Type = "floor"
    # category = "math"
    # documentation = "The floor of the input value"
    # input = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0, doc="The value to floor")
    # output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0, doc="The result of the floor")

    def execute(self, context):
        context.output.setValue(math.floor(context.input.value()))
