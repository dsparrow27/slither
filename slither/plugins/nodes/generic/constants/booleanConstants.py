from slither import api


class Boolean(api.ComputeNode):
    Type = "Boolean"
    category = "constant"
    documentation = "boolean"
    value = api.AttributeDefinition(type_=api.types.kBool, default=True, input=True)
    output = api.AttributeDefinition(type_=api.types.kBool, default=True, output=True)

    def execute(self, context):
        self.output.setValue(bool(self.input.value()))
