from slither import api


class StringNode(api.ComputeNode):
    Type = "StringNode"
    category = "constant"
    documentation = "String constant"
    value = api.AttributeDefinition(input=True, type_=api.types.kString, default="")
    output = api.AttributeDefinition(output=True, type_=api.types.kString, default="")

    def execute(self, context):
        context.output.setValue(str(context.input.value()))
