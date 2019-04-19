from slither import api


class Integer(api.ComputeNode):
    Type = "Integer"
    category = "constant"
    documentation = "integer"
    value = api.AttributeDefinition(isInput=True, type_=api.types.kInt, default=0)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kInt, default=0)

    def execute(self):
        self.output.setValue(int(self.input.value()))
