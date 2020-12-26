from slither import api


class Dictionary(api.PXComputeNode):
    Type = "dictionary"
    def compute(self, context):
        context.output.setValue(dict(context.input.value()))
