from slither import api


class StringNode(api.ComputeNode):
    Type = "string"
    def execute(self, context):
        context.output.setValue(str(context.input.value()))
