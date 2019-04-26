from slither import api


class Scalar(api.ComputeNode):
    Type = "Scalar"
    category = "constant"
    documentation = "Scalar"
    value = api.AttributeDefinition(input=True, type_=api.types.kFloat, default=0.0)
    output = api.AttributeDefinition(output=True, type_=api.types.kFloat, default=0.0)

    def execute(self, context):
        self.output.setValue(float(self.input.value()))
