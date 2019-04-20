from slither import api


class Boolean(api.ComputeNode):
    Type = "Boolean"
    category = "constant"
    documentation = "boolean"
    value = api.AttributeDefinition(type_=api.types.kBool, default=True, isInput=True)
    output = api.AttributeDefinition(type_=api.types.kBool, default=True, isOutput=True)

    def execute(self):
        self.output.setValue(bool(self.input.value()))
