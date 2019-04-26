from slither import api


class Integer(api.ComputeNode):
    Type = "Integer"
    category = "constant"
    documentation = "integer"
    value = api.AttributeDefinition(input=True, type_=api.types.kInt, default=0)
    output = api.AttributeDefinition(output=True, type_=api.types.kInt, default=0)

    def execute(self, context):
        self.output.setValue(int(self.input.value()))
