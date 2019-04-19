from slither import api


class StringNode(api.ComputeNode):
    Type = "StringNode"
    category = "constant"
    documentation = "String constant"
    value = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="")
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kString, default="")

    def execute(self):
        self.output.setValue(str(self.input.value()))
