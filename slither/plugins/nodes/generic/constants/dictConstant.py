from slither import api


class Dictionary(api.PXComputeNode):
    Type = "dictionary"
    # category = "constant"
    # documentation = "Dictionary"
    # input = api.AttributeDefinition(output=False, type_=api.types.kDict, default=dict())
    # output = api.AttributeDefinition(output=True, type_=api.types.kDict, default=dict())

    def compute(self, context):
        context.output.setValue(dict(context.input.value()))
