from slither import api


class Boolean(api.ComputeNode):
    Type = "bool"

    def execute(self, context):
        context.output.setValue(bool(context.input.value()))
