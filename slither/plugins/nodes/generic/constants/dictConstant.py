from slither import api


class Dictionary(api.ComputeNode):
    Type = "Dictionary"
    category = "constant"
    documentation = "Dictionary"
    input = api.AttributeDefinition(isOutput=False, type_=api.types.kDict, default=dict())
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kDict, default=dict())

    def execute(self, context):
        self.output.setValue(dict(self.input.value()))
